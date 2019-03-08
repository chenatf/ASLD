# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:29:53 2019

@author: chen
"""

import argparse
import subprocess
import json
import os

parser = argparse.ArgumentParser(description='Analysis the sequence data \
                                 to calculate the sgRNA distribution.')
parser.add_argument('conf', type = str, help = 'configuration file')
args = parser.parse_args()
file = args.conf

with open(file, 'r') as f:
    conf = json.load(f)
    
is_pass_md5check = True
md5file = conf['data']['md5']
with open(md5file) as fin:
    for line in fin:
        line = line.split()
        file = "{}/{}".format('/'.join(md5file.split('/')[:-1]),line[1])  
        md5 = subprocess.Popen(["md5sum",file], stdout=subprocess.PIPE)
        md5 = md5.stdout.read().decode("utf-8").split()[0] # so slow
        if md5 == line[0]:
            print('{} pass the md5 check.'.format(line[1]))
        else:
            is_pass_md5check = False
            print('{} failed the md5 check'.format(line[1]))
if is_pass_md5check:
    workspace = conf['output']['workspace']
    prefix = conf['output']['prefix']
    metadata = '{}/metadata'.format(workspace)
    result = '{}/result'.format(workspace)
    if not os.path.exists(metadata):
        os.mkdir(metadata)
    if not os.path.exists(result):
        os.mkdir(result)
    lib =  conf['data']['library']
    ref = '{}/{}.fa'.format(metadata,prefix)
    with open(conf['data']['plasmid'],'r') as fin:
        plasmid_name = fin.readline().strip()
        plasmid_seq = fin.read().strip()
    with open(lib) as fin, open(ref,'w') as fout:
        next(fin)
        for line in fin:
            line = line.strip().split(',')
            name = '>{}'.format(line[0])
            seq = plasmid_seq.replace('_', line[1])
            fout.write(name + '\n')
            fout.write(seq + '\n')
    subprocess.run(['./ASLD.sh', ref, conf['data']['read1'], conf['data']['read2'],
                    prefix, metadata, result, conf['software']['fastp'],
                    conf['software']['bwa'], conf['software']['samtools'],
                    conf['software']['bedtools'], conf['thread']['fastp'],
                    conf['thread']['bwa'], conf['thread']['samtools']])