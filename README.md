# RockhopperExecution

This profile include two small programs for execution of Rockhopper (available from http://cs.wellesley.edu/~btjaden/Rockhopper/).

The first program is 'multi_gb2ptt.py'. This program is written to combine a fasta file with more than one nodes into only one node, and annotate it for ptt format output. Rockhopper would only select the last node to analysis if more than one nodes existed in a fasta, and it might lead to failure when less than four genes exist in one node. Thus this program could solve such problems by combining nodes together.

This program requires Prokka (1.0 <= version < 2), perl, and GBKtoPTT (available from https://github.com/ajvilleg/gbk2ptt).

Usage: python multi_gb2ptt -p /path/of/prokka -e /path/of/perl -g /path/of/gbptt.pl -i /path/of/input.fasta -o /path/for/output/

Output files include ecn, err, faa, fasta, ffn, fixedproducts, fna, fsa, gbf, gff, log, ptt, sqn, tbl, txt, and val format file. Among them, fasta and ptt format files will be needed in Rockhopper analysis.

The second program is 'Rockhopper_rpkm2tpm.py'. This program is written to calculate TPM according to RPKM given by NC_999999_transcripts.txt given by Rockhopper. The calculation is based on RPKM = TPM * 1000 * total number of transcripts sampled / (read length * total number of mapped reads)

Usage: python Rockhopper_rpkm2tpm.py -i /path/of/input/

Output file with name transcripts.csv will include position information, length, strand direction, ene name, product, raw counts, normalized counts, RPKM, TPM, and expression counts.

If you have any suggestions on improving such programs, please contact me and let me know.
