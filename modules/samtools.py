import subprocess
import glob
import os

def samtools(args):
    cmd = ["singularity", "run", "--bind", args.bind, args.singularity, "/usr/miniconda3/bin/samtools", "index", "Aligned.sortedByCoord.out.bam"]

    # Index bam file
    log_file = open('samtools.log','a')
    print("Indexing bamfiles...")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=log_file)
    while process.wait() is None:
        pass
    process.stdout.close()
    log_file.close()
