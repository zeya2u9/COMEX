import os
import time
import sys
from subprocess import run
import subprocess
import datetime

WORKING_DIR = f"{os.getcwd()}"
INFO_DIR = f"{WORKING_DIR}/apkinfo"
APK_DIR = f"{WORKING_DIR}/apks"
TRACE_DIR = f"{WORKING_DIR}/perfetto_traces"

def check_battery_level():
    result = subprocess.run(['adb', 'shell', 'cat', '/sys/class/power_supply/battery/capacity'], capture_output=True, text=True)
    if result.returncode == 0:
        try:
            battery_level = int(result.stdout.strip())
            return battery_level
        except ValueError:
            pass
    return None

def path(username):
    current_path = os.getenv("PATH")
    new_path = f"/home/{username}/tools:" + current_path
    os.environ["PATH"] = new_path

    current_path = os.getenv("PATH")
    new_path1 = f"/home/{username}/tools/bin:" + current_path
    os.environ["PATH"] = new_path1

    current_path = os.getenv("PATH")
    new_path2 = f"/home/{username}/tools/lib:" + current_path
    os.environ["PATH"] = new_path2

def analyze_apk(apk_path, username):
    try:
        command = f"aapt dump badging {apk_path} | grep package:\ name"
        output = subprocess.check_output(command, shell=True, encoding='utf-8')
        print(output)
        package_name = output.split("'")[1]
        myhash = os.path.basename(apk_path).split(".")[0]
        output = f"{package_name}"
        with open(f"{WORKING_DIR}/apkinfo/{myhash}.txt", "w+") as of:
            of.write(output)
    except subprocess.CalledProcessError as e:
        print(f'Error analyzing APK: {apk_path}, {e}')
    except Exception as e:
        print(f'Error analyzing APK: {apk_path}, {e}')


def perfetto_setup(package):
    os.system(f"cat perfetto-input.example.txt | sed s/'example.package'/'{package}'/g > perfetto-input.txt")
    cmd = "adb shell perfetto -c - --txt -o /data/misc/perfetto-traces/trace < perfetto-input.txt > /dev/null 2>&1 &"
    os.system(cmd)

def perfetto_collection(maltype, package):
    os.system(f'mkdir -p {WORKING_DIR}/traces/')
    os.system(f"adb pull /data/misc/perfetto-traces/trace {WORKING_DIR}/traces/{package}.trace")
    print("Perfetto Trace pulled")


def setup():
    #atmahatya
    cmd = "adb shell cmd testharness enable"
    os.system(cmd)
    print('factory')
    print('sleeping for 20 secs')
    time.sleep(20)
    print('waiting for device')
    cmd = "adb wait-for-device"
    os.system(cmd)
    print('adb detects')
    print('sleeping for 10 secs')
    time.sleep(10)

    #auto rotate off and potrait mode on
    cmd = f"adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0"
    os.system(cmd)
    cmd = f"adb shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:0"
    os.system(cmd)

    cmd = f"adb shell settings put global bluetooth_disabled_profiles 0"
    os.system(cmd)
    cmd = "adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
    os.system(cmd)
    cmd = "adb shell settings put system show_touches 1"
    os.system(cmd)
    cmd = 'adb shell settings put global heads_up_notifications_enabled 0'
    os.system(cmd)
    time.sleep(1)

    for fil in os.listdir(f'{WORKING_DIR}/andro_essentials'):
            cmd = f"adb install -g {WORKING_DIR}/andro_essentials/{fil}"
            os.system(cmd)
            print('installing')
            time.sleep(1)

    #getting Magisk ready
    print('magisk restart for permission retentions')
    cmd = 'adb shell am start -n com.topjohnwu.magisk/.ui.MainActivity'
    os.system(cmd)
    time.sleep(2.75)
    cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_magisk.py"   #Accepts the permission and restarts the mobile.
    os.system(cmd)
    time.sleep(20)
    cmd = "adb wait-for-device"
    os.system(cmd)
    time.sleep(15)

    cmd = "adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
    os.system(cmd)

    #allowing shell permit
    os.system("adb shell su -c echo 'hello from superuser' &")
    cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_approve_root.py"
    os.system(cmd)
    print("shell permit given")

    cmd = f'monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_play_protect.py'
    os.system(cmd)

    #hiding root
    print('hiding root')
    os.system('adb uninstall com.facebook.katana')
    time.sleep(1)
    cmd = 'adb shell am start -n com.topjohnwu.magisk/.ui.MainActivity'
    os.system(cmd)
    time.sleep(2.75)
    cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_zygisk.py"
    os.system(cmd)
    time.sleep(1)
    os.system('adb reboot')
    time.sleep(10)
    cmd = "adb wait-for-device"
    os.system(cmd)
    time.sleep(15)

    cmd = f"adb install -g {apk_path}"
    os.system(cmd)
    time.sleep(2)

    #add denylist
    cmd = 'adb shell am start -n com.topjohnwu.magisk/.ui.MainActivity'
    os.system(cmd)
    time.sleep(2.75)
    cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_root_hide.py"
    os.system(cmd)
    time.sleep(1)

    cmd = "adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
    os.system(cmd)

    os.system(f'adb push {WORKING_DIR}/andro_bins/strace /data/local/tmp/')

    #connecting to wifi
    print('enabling wifi')
    cmd = "adb shell svc wifi enable"
    os.system(cmd)
    # Fill in wifi details
    cmd = "adb shell cmd -w wifi connect-network <Wifi-Username> <WIFI-Security Protocol> <WIFI-Password>"
    os.system(cmd)
    time.sleep(2)

    cmd = "adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
    os.system(cmd)

    time.sleep(1)


def donelist_update():
   # donelist = []
   os.system('touch ./script_logs/done.txt')
   with open('./script_logs/done.txt', 'r') as file:
       donelist = [line.rstrip() for line in file]
   return donelist

def completed(myhash):
   with open("./script_logs/done.txt", "a") as f:
       f.write(myhash+'\n')
   print('added {} to donelist'.format(myhash))

donelist = []
restart_message = "script starting fresh"

def metadata(myhash, username):
    apkinfo_path = f"{WORKING_DIR}/apks/{myhash}.apk"
    analyze_apk(f"{WORKING_DIR}/apks/{myhash}.apk", username)

    try:
        with open(f"{WORKING_DIR}/apkinfo"+"/"+myhash+".txt", "r") as f:
            temp = f.readline()
        return temp
    except:
        print("Metadata was not initialized")
        return False


if __name__ == "__main__":

    #Check if battery level>10
    battery_level = check_battery_level()
    while battery_level is None or battery_level < 10:
        print("Waiting for the phone to charge...")
        time.sleep(60) 
        battery_level = check_battery_level()

    if len(sys.argv) != 2:
        print("Usage: python script.py <APK_PATH>")
        sys.exit(1)

    apk_path = sys.argv[1]
    # setup("maltype_placeholder", apk_path)  

    myhash = os.path.basename(apk_path).split(".")[0]
    maltype = os.path.basename(os.path.dirname(apk_path))
    username = apk_path.split("/")[2]
    print(username)
    path(username)
    start_time = time.time()

    temp = metadata(myhash, username)
    if temp:
        package = temp
        print(package)
        print("start setup")

        # setup testbed
        setup()

        cmd = f"adb shell am start -e action start -e pcap_dump_mode pcap_file -e pcap_name {myhash}.pcap -e app_filter {package} -n com.emanuelef.remote_capture/.activities.CaptureCtrl"
        os.system(cmd)
        # time.sleep(10)
        # print('sleeping')
        cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_pcap.py"
        os.system(cmd)
        time.sleep(2)
        cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_pcap1.py"
        os.system(cmd)
        
        #perfetto start
        perfetto_setup(package)

        #app start
        # cmd = "adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
        # os.system(cmd)
        # cmd = f"adb shell am start {package}/{activity}"
        print(package)
        #cmd = f"adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1"
        #os.system(cmd)
        # time.sleep(5)
        #cmd = f"adb shell su -c lsof > {WORKING_DIR}/lsof/{myhash}-initial.csv"
        #os.system(cmd)
        # cmd = f"adb shell netstat > {WORKING_DIR}/netstat/{myhash}-initial.csv"
        # os.system(cmd)

        #cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_app_drawer.py"
        #os.system(cmd)
        starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        cmd = f"adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1"
        os.system(cmd)
        with open(f"./App_time/{myhash}.txt", "w") as file:
            file.write(f"Application {package} started at: {starttime}\n")
        print(f"main activity started") 
        time.sleep(2)
        # input("Check app started")
        #cmd = f"adb shell monkey -p com.Alredwanpublisher.ForsanAlHasob2 --throttle 200 -s 10 --pct-syskeys 0 --pct-nav 0 --pct-majornav 0 12000"
        #os.system(cmd)
        pid = str((run(f"adb shell pidof {package}".split(), capture_output=True).stdout))[2:-3]
        if pid == '':
            print('APK DID NOT START... SKIPPING')
            exit()
            # input('continue?')  
    #           completed(myhash)

        print(f"pid: {pid}")

        # cmd = f"./ramlogger.sh {myhash} {package}" 
        # os.system(cmd)

        #stracing
        cmd = f"adb shell su -c /data/local/tmp/strace -ttt -p {pid} -ff -o /data/local/tmp/{myhash}.stracelog > /dev/null 2>&1 &"
        os.system(cmd)
        cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_old_version.py"
        os.system(cmd)
        cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_approve_root.py"
        os.system(cmd)
        print("app tracing started")

        #CPU info collection started
        cmd = f"python3 cpu_info.py {myhash} &"
        os.system(cmd)

        #To capture procrank error in monkey and interupt the code
        os.system(f"timeout 60s adb shell monkey -p {package} --throttle 300 -s 10 --pct-syskeys 0 --pct-nav 0 --pct-majornav 0 1200")
        cmd = "adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
        os.system(cmd)
        # cmd = f'adb shell monkey -p {package} --throttle 300 -s 10 --pct-syskeys 0 --pct-nav 0 --pct-majornav 0 1200 > /dev/null 2>&1'
        # os.system(cmd)
        
        # slumber
        #print('sleeping now')
        #time.sleep(60)
        cmd = f"adb shell su -c lsof -p {pid} > {WORKING_DIR}/lsof/{myhash}.csv"
        os.system(cmd)

        #killing and logs retrieving
        killtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        cmd = f"adb shell su -c kill {pid} > /dev/null 2>&1 &"
        os.system(cmd)
        with open(f"./App_time/{myhash}.txt", "a") as file:
            file.write(f"Application {package} killed at: {killtime}\n")
        time.sleep(2)
        # cmd = "monkeyrunner ./monkey_scripts/monkey_approve_root.py"
        # os.system(cmd)

        print("app killed")
        #cmd = f"adb shell su -c lsof > {WORKING_DIR}/lsof/{myhash}-final.csv"
        #os.system(cmd)

        cmd = "adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
        os.system(cmd)

        cmd = f"adb shell netstat > {WORKING_DIR}/netstat/{myhash}.csv"
        os.system(cmd)
         
        #perfetto stop and log collection
        perfetto_collection(maltype, package)
        
        #Potrait mode ON
        cmd = f"adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0"
        os.system(cmd)
 
        cmd = "adb shell am start -e action stop -n com.emanuelef.remote_capture/.activities.CaptureCtrl"
        os.system(cmd)
        time.sleep(2)
        cmd = f"monkeyrunner {WORKING_DIR}/monkey_scripts/monkey_pcap_stop.py"
        os.system(cmd)
        print("pcap stopped")

        # os.system(f'mkdir -p {WORKING_DIR}/stracelogs/{maltype}/')
        os.system(f'mkdir -p {WORKING_DIR}/stracelogs/{myhash}')
        cmd = f"adb pull /data/local/tmp {WORKING_DIR}/stracelogs/{myhash}"

        os.system(cmd)
        print("stracelog pulled")

        os.system(f'mkdir -p {WORKING_DIR}/pcaps/')
        cmd = f"adb pull /sdcard/Download/PCAPdroid/{myhash}.pcap {WORKING_DIR}/pcaps"
        os.system(cmd)
        print("pcap pulled")

        cmd = f"adb shell dumpsys batterystats {package} -c > {WORKING_DIR}/batterystats/{myhash}-batterystats.csv"
        os.system(cmd)
        print("batterystats dumped")

        cmd = f"adb shell dumpsys procstats {package} -c > {WORKING_DIR}/procstats/{myhash}-procstats.csv"
        os.system(cmd)
        print("procstats dumped")
        # input("Check dropbox...")

        # dropbox pulled
        os.system(f"mkdir -p {WORKING_DIR}/dropbox/{myhash}")
        os.system("adb shell mkdir /data/local/tmp/dropbox")        
        os.system("adb shell su -c cp /data/system/dropbox/* /data/local/tmp/dropbox")
        os.system("adb shell su -c chmod 777 -R /data/local/tmp/dropbox")
        os.system(f"adb shell su -c cp -r /data/system/dropbox /sdcard/Download")
        os.system(f"adb pull /sdcard/Download/dropbox {WORKING_DIR}/dropbox/{myhash}/")

#        completed(myhash)
        print("\n\n--- APP FINISHED --- %s seconds ---\n\n" % (time.time() - start_time))
    
    else:
        print("Skipping app")
