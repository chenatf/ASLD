# ASLD (analysis sgRNA library distribution)

version 1.0.0

## Description

This program is designed to analysis the sgRNA library distribution from Illumina pair-end sequencing data.

## Quick start

1. Installation.

```bash
git clone https://github.com/chenatf/ASLD.git
```

2. Write the configuration.

Write the configuration json file like `sample.json` in the example.

3. Run the python script

```bash
python ASLD.py sample.json
```

4. Check the log file and the result csv.

## Installation

This program is tested under Ubuntu 16.04 LTS.

1. Use the conda to easy install the packages.

```bash
conda install fastp
conda install bwa
conda install samtools
conda install bedtools
conda install pandas
```

2. download the program from the github.

```bash
git clone https://github.com/chenatf/ASLD.git
```

## Configuration

```json
{
    "data": {
        "md5": "exmaple/data/sample/MD5_sample.txt",
        "library": "example/data/sample_list.csv",
        "plasmid": "example/vector/vector1.fa",
        "read1": "exmaple/data/sample/sample_1.clean.fq.gz",
        "read2": "exmaple/data/sample/sample_2.clean.fq.gz"
    },
    "output": {
        "prefix": "sample",
        "workspace": "exmaple/data/sample"
    },
    "software": {
        "fastp": "fastp",
        "bwa": "bwa",
        "samtools": "samtools",
        "bedtools": "bedtools"
    },
    "thread": {
        "fastp": "4",
        "bwa": "4",
        "samtools": "4"
    }
}
```

## Changelog

2019.03.08 Release the 1.0.0 version.

## License and citation

This program is under the MIT license.
