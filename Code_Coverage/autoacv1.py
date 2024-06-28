import os

APKDIR = "<Path to APKs>"
INFODIR="<Path to respective APKs package name in a csv>"
ACVREPORTS="<Output folder>"

if not os.path.exists(".resume"):
    print("Script Running for the first time on the folder")
    apks = os.listdir(APKDIR)
else:
    with open(".resume","r") as f:
        apks = f.read()
    apks = apks.split("\n")

for apk in apks:
    myhash = apk.split(".")[0]
    try:
        with open(INFODIR+"/"+myhash+".csv", "r") as f:
            temp = f.readline()
    except:
        continue

    temp = temp[:-1]
    package = temp.split(",")[0]
    activity = temp.split(",")[1]
    print("Instrumenting App")
    os.system("apktool empty-framework-dir")
    cmd = "acv instrument "+APKDIR+"/"+apk+" -f"
    if os.system(cmd) != 0:
        print("Apktool cant handle this apks skipping")
        apks.remove(apk)
        continue
    else:
        print("Installing app")
        cmd = "acv install <Path to instrumented APK>"
        if os.system(cmd) != 0:
            print("Cant install instrumented app, skipping")
            apks.remove(apk)
            continue
        else:
            print("Installed")
            print("Starting App and Main Activity")
            cmd = "acv start "+package+" &"
            os.system(cmd)
            os.system("sleep 3")
            cmd = "adb shell am start "+package+"/"+activity
            if os.system(cmd) != 0:
                print("Cant start main activity, skipping")
                continue
            else:
                # Replace X with time duration for which you want to run the APK
                os.system("sleep <X Seconds>")
                print("Finalizing")
                os.system("sleep 3")
                os.system("acv report "+package+" -p <Path to APK report>/"+myhash+".pickle")
                cmd = "mv -f <Path to APK report>"+package+" "+ACVREPORTS+"/"
                #print(cmd)
                os.system(cmd)
                os.system("adb uninstall "+package)
                print("DONE")
                os.system("sleep 30")
