#!/usr/bin/env python

'''
Copyright (c) 2020 RIKEN
All Rights Reserved.
See file LICENSE for details.
'''

# description: merge reference gene annotation 'gencode.vM24.annotation.gff3.gz' and TE gtf 'mm10.fa.out.high_sw_score.excld_overlap_w_ref_gene.gtf'; output gtf file 'mm10.fa.out.high_sw_score.gtf'; remove "retained_intron" from 'gencode.vM24.annotation.gff3.gz'
# 'gencode.vM24.annotation.gff3.gz' was downloaded from 'https://www.gencodegenes.org/mouse/'
# usage: python %prog
# Python 3.7.4


import gzip


d={}

# remove retained_intron
f='gencode.vM24.annotation.gtf.gz'
headers=[]
with gzip.open(f) as infile:
    for line in infile:
        line=line.decode()
        if line[0] == '#':
            headers.append(line)
        else:
            ls=line.strip().split('\t')
            for info in ls[8].split(';'):
                if 'gene_id "' in info:
                    gene_id=info
                    break
            if not gene_id in d:
                d[gene_id]=[ls[0], int(ls[3]), int(ls[4])]
            if not 'retained_intron' in line:
                d[gene_id].append(line)
headers.append('#TE_annotation_added: 2020-04-01 by Shohei KOJIMA\n')

f='mm10.fa.out.high_sw_score.excld_overlap_w_ref_gene.gtf'
with open(f) as infile:
    for line in infile:
        if not line[0] == '#':
            ls=line.strip().split('\t')
            for info in ls[8].split(';'):
                if 'gene_id "' in info:
                    gene_id=info
                    break
            if not gene_id in d:
                d[gene_id]=[ls[0], int(ls[3]), int(ls[4])]
            d[gene_id].append(line)

l=[]
for gene_id in d:
    if len(d[gene_id]) >= 4:
        l.append(d[gene_id])
l=sorted(l)

with open('mm10.fa.out.high_sw_score.gtf', 'w') as outfile:
    outfile.write(''.join(headers))
    for lis in l:
        for line in lis[3:]:
            outfile.write(line)
