import sys
import argparse
import glob
import os
import subprocess

# Wrapper for STAR alignment, HTseq-counts and DESeq2


# STAR alignment
def alignment(args):
    for f in glob.glob(f"{args.samples}/*", recursive=True):
        os.chdir(os.path.abspath(f))
        cmd = ["singularity", "run", "--bind", args.bind, args.singularity, "/STAR/source/STAR", "--runThreadN", "20", "--genomeDir", args.genomedir, "--readFilesCommand", "zcat", "--readFilesIn", "".join(glob.glob(f"{f}/*R1_001.fastq.gz")), "".join(glob.glob(f"{f}/*R2_001.fastq.gz")), "--outSAMtype", "BAM", "SortedByCoordinate", "--quantMode", "GeneCounts"]

        log_file = open('rnaseq.log','a')
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=log_file)
        while process.wait() is None:
            pass
        process.stdout.close()
        log_file.close()


# Samtool index and HTseq count
def counts(args):
    # Make results directory if it doesn't exists
    if not os.path.exists(f"{args.outputdir}/results"):
        os.makedirs(f"{args.outputdir}/results")

    # Loop through sample dir and do counts
    for f in glob.glob(f"{args.samples}/*", recursive=True):
        os.chdir(os.path.abspath(f))

        # Filename of output file with counts
        filename = f"{args.outputdir}/results/"+os.path.basename(f)+".counts"

        cmd1 = ["singularity", "run", "--bind", args.bind, args.singularity, "/usr/miniconda3/bin/samtools", "index", "Aligned.sortedByCoord.out.bam"]


        gtf = "".join(glob.glob(f"{args.genomedir}/*.gtf")) # Full path to gtf file in genome diretory
        cmd2 = (f"singularity run --bind {args.bind} {args.singularity} /usr/miniconda3/bin/htseq-count -m union -r pos -a 10 --stranded=no -f bam -r pos Aligned.sortedByCoord.out.bam {gtf} > {filename}")

        # Index bam file
        log_file = open('rnaseq.log','a')
        print("Indexing bamfiles...")
        process1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=log_file)
        while process1.wait() is None:
            pass
        process1.stdout.close()

        # Count file
        log_file = open('rnaseq.log','a')
        print("Counting...")
        process2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=log_file, shell=True)
        while process2.wait() is None:
            pass
        process2.stdout.close()

        log_file.close()


def merge_counts(args):
    # Merge the count files for prep to DESeq2
    pass


def deseq(args):
    # Run R script for DEseq (module)
    pass


def arg():
    parser = argparse.ArgumentParser(prog=sys.argv[0], description="wrapper for RNAseq")
    parser.add_argument("-v", "--verbose", action="store_true", help="Be more verbose")
    parser.add_argument("-p", "--samples", help="Path to diretory with diretories of samples")
    parser.add_argument("-b", "--bind", help="Path to diretory with diretories to include in singularity")
    parser.add_argument("-s", "--singularity", help="Path to singularity image")
    parser.add_argument("-g", "--genomedir", help="Path to genomedir for STAR")
    parser.add_argument("-o", "--outputdir", help="Outputdir for count results")

    args = parser.parse_args()

    return args

def main():
    args = arg()
    alignment(args)
    counts(args)


if __name__ == "__main__":
    main()
