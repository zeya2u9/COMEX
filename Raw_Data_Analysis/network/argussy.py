import os
import subprocess

def pcaptoargus(directory=None):
    # Get the current directory if not specified
    if directory is None:
        directory = os.getcwd()
    
    print(f"Current Directory: {directory}")
    
    # Create output directories
    argus_out_dir = os.path.join(directory, "argusout")
    csv_out_dir = os.path.join(directory, "csvout")
    os.makedirs(argus_out_dir, exist_ok=True)
    os.makedirs(csv_out_dir, exist_ok=True)
    
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pcap"):
                print(f"Processing {file}...")
                
                argus_file = os.path.join(argus_out_dir, file[:-5] + ".argus")
                csv_file = os.path.join(csv_out_dir, file[:-5] + ".csv")
                
                # Create the command to convert pcap to argus
                pcapfiletoargus = ["argus", "-r", os.path.join(root, file), "-w", argus_file]
                
                # Create the command to convert argus to csv
                argustocsv = [
                    "ra", "-s", "srcid, stime, ltime, sstime, dstime, sltime, dltime, trans, seq, flgs, dur, avgdur, stddev, mindur, maxdur, saddr, daddr, proto, sport, dport, stos, dtos, sdsb, ddsb, sco, dco, sttl, dttl, sipid, dipid, smpls, dmpls, svlan, dvlan, svid, dvid, svpri, dvpri, spkts, dpkts, sbytes, dbytes, sappbytes, dappbytes, sload, dload, sloss, dloss, sploss, ploss, srate, drate, smac, dmac, dir, sintpkt, dintpkt, sjit, djit, state, suser, duser, swin, dwin, trans, srng, erng, stcpb, dtcpb, tcprtt, inode, offset, smaxsz, dmaxsz, sminsz, dminsz",
                    "-r", argus_file, "-c", ","
                ]
                
                # Run the pcap to argus conversion
                subprocess.call(pcapfiletoargus)
                
                # Run the argus to csv conversion
                with open(csv_file, "w") as f:
                    result = subprocess.run(argustocsv, stdout=f, stderr=subprocess.PIPE, text=True)
                    
                # Check for errors
                if result.stderr:
                    print(f"Error processing {file}: {result.stderr}")

def main():
    pcaptoargus()  # Optionally, pass a directory as an argument

if __name__ == "__main__":
    main()
