# RNAseq project

___

|||
|---|---|  
|<img style="float: right;" src="https://user-images.githubusercontent.com/42669709/199463366-7233de42-27a2-4e0c-88d0-307d0422445d.svg" width="500" height="500">| 1. Starting with alignment of fastq files <br/> - [STAR](https://github.com/alexdobin/STAR) <br/> 2. Index bam files by using samtools <br/> - [samtools](http://www.htslib.org/doc/samtools-sort.html) <br/> 3. Given a file with aligned sequencing reads and a list of <br/>  genomic features, count how many reads map to each feature. <br/> - [HTSeq-count](https://htseq.readthedocs.io/en/release_0.11.1/count.html) <br/> 4. Merging count files from HTSeq count to one big matrix <br/>  5. Run DESeq2 using the `counts.txt` file from previous step <br/> - [DESeq2](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0550-8) |

___

## How to run
___
- Clone this repository
- Download singularity image

### Run
___
`python3 wrapper.py --samples [PATH_TO_SAMPLEDIR] --bind [PATH_TO_DIRS_TO_INCLUDE] --genomedir [PATH_TO_GENOMEFILES] --singularity [PATH_TO_SINGULARITY_IMAGE] --outputdir [OUTPUT_COUNTFILES]` 

```
--samples                     The samples directory should have diretories 
                              with name of the sample and the fastq files in every 
                              sample dir -> Samples/sample/*fastq.gz
                              
--bind                        Path to which directories you want to include 
                              in your singularity (should be atleast samples directory and output) 
                              
--genomedir                   Path to your genome fasta and gtf file and index files

--singularity                 Path to the singularity image

--outputdir                   Path to output from HTSeq-count, the script 
                              will create a directory called "results" in this path

```



## Dependencies
___

|Program|Version|
|--|--|
|Singularity|3.5.2|
|STAR|2.7.10a|
|samtools|1.6|
|htslib|1.6|
|HTSeq-count|2.0.2|
|DESeq2|1.36.0|
|pandas|1.5.0|
