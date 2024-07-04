from multiprocessing import Process
import os
import time
import pandas as pd
import sys

# if len(sys.argv) < 3:
#       sys.exit('androzoo_script.py <PT number> <number of threads for stress test>')

# pt_num = int(sys.argv[1])
# stress = int(sys.argv[2])

sys.exit("ADD YOUR API KEY AND REMOVE EXIT()")
apikey = "<YOUR API KEY HERE>"

def download_from_hash(thread_num, hash_list, num_hashes):

        print("Process number " + str(thread_num) + " executing.")
        my_list = [hash_list[my_hash] for my_hash in range((num_hashes//40)*thread_num, (num_hashes//40)*(thread_num+1) if thread_num!=39 else num_hashes)]

        for my_hash in my_list:

                print("Downloading hash " + my_hash)
                os.system(f"curl -O --remote-header-name -G -d apikey={apikey} -d sha256={my_hash} https://androzoo.uni.lu/api/download")

                time.sleep(5)


if __name__ == "__main__":

        # for year in ["2018", "2019", "2020", "2021", "2022"]:

        # virus_csv = pd.read_csv(f'{os.getenv("HOME")}/Downloads/Androzoo_yearwise/virus/virus_{year}.csv')
        # benign_csv = pd.read_csv(f'{os.getenv("HOME")}/Downloads/Androzoo_yearwise/benign/benign_{year}.csv')
        # viruses = virus_csv.iloc[:, 0]
        # benigns = benign_csv.iloc[:, 0]

        # new_csv = open(f'{os.getenv("HOME")}/Downloads/Androzoo_yearwise/virus/virus_{year}_hashes.txt', 'w')
        # for i in range(len(viruses)):
        #       new_csv.write(viruses[i] + "\n") 
        # new_csv.close()

        # new_csv = open(f'{os.getenv("HOME")}/Downloads/Androzoo_yearwise/benign/benign_{year}_hashes.txt', 'w')
        # for i in range(len(benigns)):
        #       new_csv.write(benigns[i] + "\n") 
        # new_csv.close()


        # print(viruses)
        # exit()

        # viruses.to_csv()
        # benigns.to_csv()

        # myprocesses = []
        # num_hashes = len(viruses)

        # for i in range(40):
        #       myprocesses.append(Process(target=download_from_hash, args=(i, viruses, num_hashes)))
        #       myprocesses[i].daemon=True
        #       myprocesses[i].start()

        # for i in range(40):
        #       myprocesses[i].join()

        # os.system(f"mkdir -p {os.getenv('HOME')}/MalwareDownloads/Androzoo/Androzoo_yearwise/virus/virus_{year}")
        # os.system(f"mv ./*.apk {os.getenv('HOME')}/MalwareDownloads/Androzoo/Androzoo_yearwise/virus/virus_{year}")

        # os.system(f"mkdir -p /home/nsl400/Downloads/Androzoo_yearwise/benign30k/")
        # myprocesses.clear()

        with open(f"{os.getenv('HOME')}/Desktop/missing_androzoo.txt", 'r') as fd1:
                benigns = [line.strip() for line in fd1]

        num_hashes = len(benigns)

        for i in range(40):
                myprocesses.append(Process(target=download_from_hash, args=(i, benigns, num_hashes)))
                myprocesses[i].daemon=True
                myprocesses[i].start()

        for i in range(40):
                myprocesses[i].join()


        # os.system(f"mv ./*.apk {os.getenv('HOME')}/MalwareDownloads/Androzoo/Androzoo_yearwise/benign/benign_{year}")


        print('\n\n----------------------------Execution over--------------------------\n')

