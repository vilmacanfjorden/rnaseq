import subprocess
import glob
import os


# Samtools index
def samtools(args):
    cmd = ["singularity", "run", "--bind", args.bind, args.singularity, "/usr/miniconda3/bin/samtools", "index", "Aligned.sortedByCoord.out.bam"]

    # Index bam file
    print("Indexing bamfiles...")
    log_file = open("rna_pipline.log","a")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=log_file)
    while process.wait() is None:
        pass
    process.stdout.close()
    log_file.close()
