import subprocess
import glob
import os
import pandas as pd

# HTseq count
def merge_counts(args):
    # Filename of files with counts and sort filenames
    filenames = sorted(glob.glob(f"{args.outputdir}/results/*.counts", recursive=True))

    # Merge count files
    print("Merging count files...")

    frames = []
    header = ["ENSEMBL_ID"]
    # Loop through names in dir to get data
    for m in filenames:
        h = os.path.basename(m.replace(".counts", "")) # Get name from headers
        header.append(h)

        values = pd.read_csv(m, sep="\t", index_col=0, header=None) # Get values make ENSEMBL_ID to index to remove duplicate columns
        frames.append(values)

    df = pd.concat(frames, axis=1) # Concatenate the data from different files
    df.reset_index(inplace=True, level=0) # Remove index
    df.columns = header # Add the headers (sample names)
    df.to_csv(f"{args.outputdir}/results/counts.txt", sep=" ", index=False) # Write dataframe to a txt file
