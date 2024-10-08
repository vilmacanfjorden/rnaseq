import argparse
import glob
import os
from time import time
import datetime
from functools import wraps


# Wrapper for STAR alignment, HTseq-counts and DESeq2
import modules.alignment as align
import modules.samtools as sam
import modules.count as count
import modules.merge_counts as mc


# Time decorator
def timing(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        now = datetime.datetime.now()
        start = time()
        result = function(*args, **kwargs)
        end = time()
        fh = open("time.log", "a")
        lines_of_text = now.strftime("%Y-%m-%d %H:%M") + "\n" \
                + os.path.basename(os.getcwd()) + "\n" \
                + "Function: " \
                + function.__name__ + "\n" \
                + "Elapsed time: {}".format(end-start) \
                + " seconds \n" \
                + "********************************************** \n" 
        fh.writelines(lines_of_text)
        fh.close()
        return result
    return wrapper


# STAR alignment
@timing
def alignment(args,f):
    align.alignment(args,f)


# Samtools index
@timing
def index(args):
    sam.samtools(args)


# HTseq count
@timing
def counts(args,f):
    count.count(args,f)


# Merge count files
@timing
def merge_counts(args):
    mc.merge_counts(args)  # Merge the count files for prep to DESeq2


def deseq(args):
    # Run R script for DEseq (module)
    pass


def arg():
    parser = argparse.ArgumentParser(description="wrapper for RNAseq")
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
    # Make results directory if it doesn't exists
    if not os.path.exists(f"{args.outputdir}/results"):
        os.makedirs(f"{args.outputdir}/results")

    # Loop through all sample directories 
    for f in glob.glob(f"{args.samples}/*", recursive=True):
        os.chdir(os.path.abspath(f))
        alignment(args,f) # Align fastq files using STAR
        index(args) # Index bam files using samtools
        counts(args,f) # Create counts with Htseq count
    merge_counts(args) # Merge count files

if __name__ == "__main__":
    main()
