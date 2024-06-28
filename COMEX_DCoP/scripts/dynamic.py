import os
import pandas as pd
import time
import queue
import random
import threading
import csv
import json
import subprocess

'''
To restart testbed from scratch:
1. Delete counters.json
2. Clear benign_done.txt and malware_done.txt
'''


# Global variables ------------------------------------------------------------------
vm_info = {	

    "<Device1-ID>": {"ip": "<VM1-IP>", "username": "<VM1-Username>", "password": "<VM1-Password>"},
    "<Device2-ID>": {"ip": "<VM2-IP>", "username": "<VM2-Username>", "password": "<VM2-Password>"},
    # Add more information about device and their corresponding VM's to add more devices to COMEX
}

# To add more devices add device ID's in free_workers list to COMEX
free_workers = ["<Device1-ID>", "<Device2-ID>"]
master_queue = queue.Queue()

def execute_remote_python_script(hostname, username, password, script_path, hash):
    try:
        sshpass_command = f'sshpass -p {password} ssh {username}@{hostname}'
        dire = f'cd /home/{username}/Desktop/testbed'
        cmd = f'{sshpass_command} {dire}'
        subprocess.check_output(cmd, shell = True)
        python_command = f'python3 {script_path} /home/{username}/Desktop/testbed/apks/{hash}.apk'
        full_command = f"{sshpass_command} 'cd /home/{username}/Desktop/testbed && {python_command}'"
        subprocess.check_output(full_command, shell=True)
        # print(output.decode())

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def scp_apk(server_ip, server_username, server_password, remote_file_path, local_directory, vm_ip, vm_username, vm_password, vm_file_directory):
    def extract_hash_from_filename(filename):
        parts = filename.split('.')
        if len(parts) >= 2:
            return parts[0]
        else:
            return None

    local_file_path = os.path.join(local_directory, os.path.basename(remote_file_path))
    scp_command_server_to_local = f"sshpass -p '{server_password}' scp {server_username}@{server_ip}:{remote_file_path} {local_file_path}"
    subprocess.run(scp_command_server_to_local, shell=True)

    apk_filename = os.path.basename(remote_file_path)
    hash_value = extract_hash_from_filename(apk_filename)
    if hash_value is None:
        print("Failed to extract hash from APK filename.")
        return

    vm_file_path = os.path.join(vm_file_directory, hash_value + ".apk")
    scp_command_local_to_vm = f"sshpass -p '{vm_password}' scp {local_file_path} {vm_username}@{vm_ip}:{vm_file_path}"
    subprocess.run(scp_command_local_to_vm, shell=True)

    print("APK file transferred successfully from server to VM.")

#To add more families to COMEX add metadata here
family_targets = {
	"<Family 1>": <Count of family1 APKs in a year>,
	"<Family 2>": <Count of family2 APKs in a year>,
}
year_target = <Sum of family counts>


def load_counters(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            counters = json.load(file)
            # Convert year keys to integers for benign counters
            for year_str in list(counters["benign"].keys()):
                counters["benign"][int(year_str)] = counters["benign"].pop(year_str)
            # Convert year keys to integers for malware counters
            for family, year_dict in counters["malware"].items():
                for year_str in list(year_dict.keys()):
                    year_dict[int(year_str)] = year_dict.pop(year_str)
            return counters
    else:
        return {
            "benign": {year: 0 for year in [2019, 2020, 2021]},
            "malware": {family: {year: 0 for year in [2019, 2020, 2021]} for family in family_targets.keys()}
        }


COUNTERS_DIR = "~/COMEX/COMEX_DCoP/scripts/crash_resume"
counters = load_counters(f'{COUNTERS_DIR}/counters.json')

def save_counters(counters, filename):
    with open(filename, 'w') as file:
        json.dump(counters, file)

malware_lock = threading.Lock()
benign_lock = threading.Lock()

'''
{
  "benign": {
	2019: [(md5_hash, path), (md5_hash, path), ...],
	2020: [(md5_hash, path), (md5_hash, path), ...],
	2021: [(md5_hash, path), (md5_hash, path), ...]
  }
}

{
  "malware": {
	"family1": {
	  2019: [(md5_hash, path), (md5_hash, path), ...],
	  2020: [(md5_hash, path), (md5_hash, path), ...],
	  2021: [(md5_hash, path), (md5_hash, path), ...]
	},
	"family2": {
	  2019: [(md5_hash, path), (md5_hash, path), ...],
	  2020: [(md5_hash, path), (md5_hash, path), ...],
	  2021: [(md5_hash, path), (md5_hash, path), ...]
	},
	...
  }
}

'''

def read_csv(filepath):
	data = []
	with open(filepath, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data.append((row['md5_hash'], row['path']))
	return data



def populate_database(root_dir):
	database = {"benign": {}, "malware": {}}

	for category in ["benign", "malware"]:
		category_dir = os.path.join(root_dir, category)
		for filename in os.listdir(category_dir):
			if filename.endswith(".csv"):
				year = int(filename.split("_")[0].split(".")[0])
				if category == "benign":
					database["benign"][year] = []
				else:
					family = filename.split("_")[1].split(".")[0]
					if family not in database["malware"]:
						database["malware"][family] = {}
					database["malware"][family][year] = []

				with open(os.path.join(category_dir, filename), newline="") as csvfile:
					reader = csv.reader(csvfile)
					next(reader)  # Skip header row
					for row in reader:
						if category == "benign":
							database["benign"][year].append((row[0], row[2]))  #md-5 hash, path
						else:
							database["malware"][family][year].append((row[0], row[4]))  #md-5 hash, path

	return database

root_directory = "~/COMEX/COMEX_DCoP/metadata"
database = populate_database(root_directory)

'''
For benign tasks:

	task[0] "benign".
	task[1] year of the APK.
	task[2] MD5 hash of the APK.
	task[3] file path of the APK.

For malware tasks:

	task[0] "malware".
	task[1] year of the APK.
	task[2] MD5 hash of the APK.
	task[3] file path of the APK.
	task[4] family of the malware.
'''
# Global variables defined ----------------------------------------------------------



def add_hash_to_file(hash_value, apktype): 
	file_path=f"~/COMEX/COMEX_DCoP/crash_resume/{apktype}_done.txt"
	with open(file_path, 'a') as file:
		file.write(hash_value.upper() + '\n')
		file.close()

def check_hash_in_file(hash_value, apktype):
	file_path=f"~/COMEX/COMEX_DCoP/crash_resume/{apktype}_done.txt"
	with open(file_path, 'r') as file:
		for line in file:
			# print(f"Line found in {apktype}: {hash_value}")
			if hash_value.upper() in line.strip():
				file.close()
				return True
	file.close()
	return False


class BenignTaskDispatcher(threading.Thread):
	
	def __init__(self, benign_tasks):
		super().__init__()
		self.benign_tasks = benign_tasks
		self.task = None
		self.available = False
		self.thread_state = "alive"


	def run(self):
		while True:
			for year in [2019, 2020, 2021]:
				# print(counters["benign"][year])
				# input()
				if (	
						(counters["benign"][year] >= year_target and 
						len(self.benign_tasks[year]) > 0) or
						check_hash_in_file(hash_value=self.benign_tasks[year][0][0], apktype="benign")

					):		
					# input(f":::HASH FOUND {self.benign_tasks[year][0][0]}////////\n \n \n \n \n")
					
					self.benign_tasks[year].pop(0)
					continue

				with benign_lock:
					self.available = True
					self.task = ["benign", year] + list(self.benign_tasks[year].pop(0))
					add_hash_to_file(hash_value=self.task[2], apktype="benign")
					self.log(f"{self.task} available.")

				while True:
					benign_lock.acquire()
					if not self.available:
						benign_lock.release()
						break
					benign_lock.release()

				if (	all(value >= year_target for value in counters["benign"].values()) or
						all(not self.benign_tasks[year] for year in [2019, 2020, 2021])
					):
					
					self.thread_state = "dead"
					break

		self.log("BenignTaskDispatcher thread terminated.")


	def give(self):
		while True:
			benign_lock.acquire()
			if self.available:
				benign_lock.release()
				break
			benign_lock.release()

		with benign_lock:
			self.available = False
			temp = self.task

		return temp


	def log(self, message):
		print(f"[BTD]: {message}")


class MalwareTaskDispatcher(threading.Thread):
	
	def __init__(self, malware_tasks):
		super().__init__()
		self.malware_tasks = malware_tasks
		self.task = None
		self.available = False
		self.thread_state = "alive"

	def run(self):
	    while True:
	        for family in family_targets.keys():
	            for year in [2019, 2020, 2021]:
	                try:
	                    # Print the current family, year, and count of tasks
	                    task_count = len(self.malware_tasks[family][year])
	                    # print(f"Processing Family: {family}, Year: {year}, Task Count: {task_count}")
	                    
	                    if (counters["malware"][family][year] >= family_targets[family] and task_count > 0) or check_hash_in_file(hash_value=self.malware_tasks[family][year][0][0], apktype="malware"):
	                        self.malware_tasks[family][year].pop(0)
	                        continue

	                    with malware_lock:
	                        self.available = True
	                        self.task = ["malware", year] + list(self.malware_tasks[family][year].pop(0)) + [family]
	                        add_hash_to_file(hash_value=self.task[2], apktype="malware")
	                        self.log(f"{self.task} available.")

	                    while True:
	                        malware_lock.acquire()
	                        if not self.available:
	                            malware_lock.release()
	                            break
	                        malware_lock.release()

	                except IndexError:
	                    print(f"IndexError encountered. Family: {family}, Year: {year}")
	                except KeyError:
	                    print(f"KeyError: Family: {family}, Year: {year} not found in tasks or counters")

	        if (all(all(value >= target for value in counters["malware"][family].values()) for family, target in family_targets.items()) or
	                all(not self.malware_tasks[family][year] for family in family_targets.keys() for year in [2019, 2020, 2021])):
	            self.thread_state = "dead"
	            break

	    self.log("MalwareTaskDispatcher thread terminated.")


	def give(self):
		while True:
			malware_lock.acquire()
			if self.available:
				malware_lock.release()
				break
			malware_lock.release()

		with malware_lock:
			self.available = False
			temp = self.task

		return temp

	def log(self, message):
		print(f"[MTD]: {message}")


class PhoneWorkerThread(threading.Thread):
	# constructor
	def __init__(self, worker_id):
		super().__init__()
		self.worker_id = worker_id
		
		self.app_type = None
		self.app_year = None
		self.malware_family = None
		self.app_hash = None
		self.app_path = None 
		self.analysis_start_time = None
		self.skip_current_task = False
		
	def run(self):
		self.analysis_start_time = time.time() 
		vm_information = vm_info.get(self.worker_id)
		if vm_information:
			vm_ip = vm_information['ip']
			vm_username = vm_information['username']
			vm_password = vm_information['password']
			vm_file_directory = f"<APK file directory in VM>"
			local_directory = "<APK file directory on local host>"
			remote_path = self.app_path
			server_username = "<APK database username>"
			server_password = "<APK database password>"
			server_ip = None
			app_hash = os.path.basename(remote_path).split(".")[0]
			try:
				print("SCP'ing from server to VM")
				print(server_ip, server_username, server_password, remote_path, local_directory, vm_ip, vm_username, vm_password, vm_file_directory)
				scp_apk(server_ip, server_username, server_password, remote_path, local_directory, vm_ip, vm_username, vm_password, vm_file_directory)
				self.log(f"APK file transferred successfully to VM {self.worker_id}")
				execute_remote_python_script(vm_ip, vm_username, vm_password, f'/home/{vm_username}/Desktop/testbed/raw_testbed.py', app_hash)

			except Exception as e:
				#print(server_ip, server_username, server_password, remote_path, local_directory, vm_ip, vm_username, vm_password, vm_file_directory)
				self.log(f"Failed to transfer APK file to VM {self.worker_id}: {str(e)}")

		self.log(f"Worker {self.worker_id} is working")
		time.sleep(random.randint(9,12)) # Simulating work
		self.log(f"Worker {self.worker_id} finished work")
		free_workers.append(self.worker_id)

		if self.is_analysis_timed_out():
			self.log(f"Analysis timed out for worker {self.worker_id}. Skipping current task.")
			self.skip_current_task = True
			return

		# work done
		self._counterUpdate(app_hash)
		'''
		'''
		# pass

	def is_analysis_timed_out(self):
		return time.time() - self.analysis_start_time > 540

	def setWorkerVariables(self, app_info):
		self.app_type = app_info[0]
		self.app_year = app_info[1]
		self.app_hash = app_info[2]
		self.app_path = app_info[3]
		if self.app_type == "malware":
			self.malware_family = app_info[4]


	def _counterUpdate(self, hash):
		'''		update counterws for reference of task dispenser
				take checking functinalirty from early testbed
		'''
		fruit = True
		file_command = f"ls ~/COMEX/COMEX_AXMoD/batterystats/{hash}-batterystats.csv"
		full_command = f"{file_command}"
		file_present = subprocess.check_output(full_command, shell=True)
		if b"No such file or directory" in file_present:
			fruit = False
		
		if fruit:
			# save_counters(counters, f"{COUNTERS_DIR}/counters.json")
			if self.app_type == "benign":
				counters[self.app_type][self.app_year] += 1
			else:
				counters[self.app_type][self.malware_family][self.app_year] += 1
			save_counters(counters, f"{COUNTERS_DIR}/counters.json")

			self.log(f"counter of {self.app_type} {self.app_year} {self.app_hash} increased to {counters[self.app_type][self.app_year] if self.app_type == 'benign' else counters[self.app_type][self.malware_family][self.app_year]}") ######################### debug
		else:
			self.log(f"Failed to bear fruit")


	def log(self, message):
		print(f"[PWT]:\n[\n\t{self.worker_id}\n\t{self.app_type}\n\t{self.app_year}\n\t{self.app_hash}\n\t{self.malware_family or 'None'}\n] : {message}\n")


class MasterThread(threading.Thread):
	def __init__(self, master_id, task_dispatcher):
		super().__init__()
		self.master_id = master_id
		self.task_dispatcher = task_dispatcher

	def run(self):
		while self.task_dispatcher.thread_state == "alive":
			master_queue.put(self.master_id)  # Add master to the queue
			while master_queue.queue[0] != self.master_id:  # Wait for turn
				pass
			while not free_workers:  # Wait if no free workers available
				pass
			print(free_workers)
			# exit()
			worker_id = free_workers.pop(0)
			print(free_workers)
			# exit()
			worker = PhoneWorkerThread(worker_id)
			
			task_info = self.task_dispatcher.give()

			worker.setWorkerVariables(task_info)
			self.log(f"{self.master_id} assigned task to worker {worker_id} :\n{task_info}")
			worker.start()

			
			master_queue.get()  # Remove master from the queue

	def log(self, message):
		print(f"-----------------------------------------------------------------\n[{'BMT' if self.master_id == 'Benign Master' else 'MMT'}]: {message}\n-----------------------------------------------------------------\n")



if __name__=="__main__":

	benign_td = BenignTaskDispatcher(database["benign"])
	benign_td.start()
	malware_td = MalwareTaskDispatcher(database["malware"])
	malware_td.start()

	master1 = MasterThread("Benign Master", benign_td)
	master2 = MasterThread("Malware Master", malware_td)

	master1.start()
	master2.start()

	master1.join()
	master2.join()
