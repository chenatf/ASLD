#!/bin/bash

ref=${1}
r1=${2}
r2=${3}
prefix=${4}
metadata=${5}
result=${6}
fastp_path=${7}
bwa_path=${8}
samtools_path=${9}
bedtools_path=${10}
fastp_thread=${11}
bwa_thread=${12}
samtools_thread=${13}

mapping_ratio()
{
    all_result=$(${samtools_path} view -c "${1}")
    no_alighnment=$(${samtools_path} view -c -f 4 "${1}")
    no_primany=$(${samtools_path} view -c -f 2304 "${1}")
    all_read=$(expr ${all_result} - ${no_primany})
    mapping_reads=$(expr ${all_read} - ${no_alighnment})
    ratio=$(expr 100 \* ${mapping_reads} / ${all_read})
    echo "All reads are:${all_read}  Mapping reads:${mapping_reads}  mapping ratio:${ratio}%"
}

main()
{
    ## quality control
    ${fastp_path} -w ${fastp_thread} -c \
    -h "${metadata}/${prefix}.fastp.html" -j "${metadata}/${prefix}.fastp.json" \
    -i "${r1}" -o "${metadata}/${prefix}_r1.fq.gz" \
    -I "${r2}" -O "${metadata}/${prefix}_r2.fq.gz"
    ## mapping the sequence data to the reference
    ${bwa_path} index ${ref}
    ${bwa_path} mem -t ${bwa_thread} ${ref} \
    ${metadata}/${prefix}_r1.fq.gz \
    ${metadata}/${prefix}_r2.fq.gz | ${samtools_path} view -bS - > "${metadata}/${prefix}.bam"
    ${samtools_path} sort -@ ${samtools_thread} -o "${metadata}/${prefix}.sorted.bam" "${metadata}/${prefix}.bam"
    ${samtools_path} index "${metadata}/${prefix}.sorted.bam"
    ## mapping ratio
    mapping_ratio "${metadata}/${prefix}.sorted.bam"
    ## calculate coverage
    ${bedtools_path} genomecov -pc -bga -ibam "${metadata}/${prefix}.sorted.bam" > "${metadata}/${prefix}.bed"
    ## summary
    python summary_library.py "${metadata}/${prefix}.bed" "${result}/${prefix}.csv"   
}

main > "${result}/${prefix}.log" 2>&1 &
 