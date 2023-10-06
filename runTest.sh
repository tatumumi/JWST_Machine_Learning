f = open("sub.sh", 'w')
    f.write("#!/bin/bash\n")
    f.write("#SBATCH --job-name=example\n")
    f.write("#SBATCH --partition=shared\n")
    f.write("#SBATCH --time=0-02:00:00 ## time format is DD-HH:MM:SS\n")
    f.write("#SBATCH --nodes=1\n")
    f.write("#SBATCH --cpus-per-task=1\n")
    f.write("#SBATCH --mem=10G # Memory per node my job requires\n")
    f.write("#SBATCH --error=example-%A.err # %A - filled with jobid, where to write the stderr\n")
    f.write("#SBATCH --output=example-%A.out # %A - filled with jobid, wher to write the stdout\n")
    f.write("source ~/.bash_profile\n")
    f.write("cd /home/tatumumi/supernova_lts/JWST_Machine_Learning\n")
    f.write("python runTest.py training_patches.pickle")
    f.close()