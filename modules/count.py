import subprocess
import glob
import os


# HTseq count
def count(args,f):
    # Filename of output file with counts
    filename = f"{args.outputdir}/results/"+os.path.basename(f)+".counts"

    gtf = "".join(glob.glob(f"{args.genomedir}/*.gtf")) # Full path to gtf file in genome diretory
    cmd = (f"singularity run --bind {args.bind} {args.singularity} /usr/miniconda3/bin/htseq-count -m union -r pos -a 10 --stranded=no -f bam -r pos Aligned.sortedByCoord.out.bam {gtf} > {filename}")

    # Count files
    print("Counting...")
    log_file = open("rna_pipeline.log", "a")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=log_file, shell=True)
    while process.wait() is None:
        pass
    process.stdout.close()
    log_file.close()
