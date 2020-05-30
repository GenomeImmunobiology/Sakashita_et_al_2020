#!/bin/bash

# Copyright (c) 2020 RIKEN
# All Rights Reserved.
# See file LICENSE for details.

# description: prepare non-overlapping TE and reference gene annotation
# GNU bash, version 4.4.19(1)-release (x86_64-pc-linux-gnu)
# bedtools v2.26.0


# download data
# 'mm10.fa.out.gz' was downloaded from 'http://www.repeatmasker.org/species/mm.html'
wget http://www.repeatmasker.org/genomes/mm10/RepeatMasker-rm405-db20140131/mm10.fa.out.gz
# 'gencode.vM24.annotation.gff3.gz' was downloaded from 'https://www.gencodegenes.org/mouse/'
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M24/gencode.vM24.annotation.gff3.gz
# download 'gencode.vM24.annotation.gtf.gz' from https://www.gencodegenes.org/mouse/, on 2020 04 01, GRCm38.p6
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M24/gencode.vM24.annotation.gtf.gz


# only TE annotation, convert to gtf
zcat gencode.vM24.annotation.gff3.gz | grep -v retained_intron | grep $'\t'exon$'\t' > gencode.vM24.annotation.exon.gff3
python remove_low_SW_score.py  # fa.out to gtf
head -n 1 mm10.fa.out.high_sw_score.gtf > mm10.fa.out.high_sw_score.excld_overlap_w_ref_gene.gtf
bedtools subtract -A -a mm10.fa.out.high_sw_score.gtf -b gencode.vM24.annotation.exon.gff3 >> mm10.fa.out.high_sw_score.excld_overlap_w_ref_gene.gtf


# merge TE gtf and reference gene gtf
python remove_retained_intron.py  # merge ref gtf and TE annotations


# remove unnecessary files
rm gencode.vM24.annotation.exon.gff3 mm10.fa.out.high_sw_score.gtf
