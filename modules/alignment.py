import glob
import subprocess


# STAR alignment
def alignment(args,f):
    cmd = ["singularity", "run", "--bind", args.bind, args.singularity, "/STAR/source/STAR", "--runThreadN", "20", "--genomeDir", args.genomedir, "--readFilesCommand", "zcat", "--readFilesIn", "".join(glob.glob(f"{f}/*R1_001.fastq.gz")), "".join(glob.glob(f"{f}/*R2_001.fastq.gz")), "--outSAMtype", "BAM", "SortedByCoordinate", "--quantMode", "GeneCounts"]

    # Aligning files
    print("Aligning...")
    log_file = open("rna_pipeline.log","a")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=log_file)
    while process.wait() is None:
        pass
    process.stdout.close()
    log_file.close()
