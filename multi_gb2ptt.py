import argparse
import os

parser = argparse.ArgumentParser(description='This program is written to combine a fasta file with more than one nodes '
                                             'into only one node, and annotate it for ptt format output. \n'
                                             'Usage: python multi_gb2ptt -p /path/of/prokka -e /path/of/perl -g '
                                             '/path/of/gbptt.pl -i /path/of/input.fasta -o /path/for/output/')
parser.add_argument('-p', '--prokka', type=str, help='path of prokka installed, 1.0 <= version < 2')
parser.add_argument('-e', '--perl', type=str, help='path of perl installed')
parser.add_argument('-g', '--gbptt', type=str, help='path of GBKtoPTT.pl download. Available from '
                                                    'https://github.com/ajvilleg/gbk2ptt')
parser.add_argument('-i', '--input', type=str, help='path of input fasta format file')
parser.add_argument('-o', '--outdir', type=str, help='path of output folder')
args = parser.parse_args()

infh = open(args.input)
outdir = args.outdir
if outdir.split('/')[-1] != '':
    outdir += '/'
os.system('mkdir -p ' + outdir)
out_path = outdir + 'NODE.fasta'
outfh = open(out_path, 'w')
outfh.write('>NODE\n')
for line in infh:
    if '>' in line:
        outfh.write('N' * 60 + '\n')
    else:
        outfh.write(line)
infh.close()
outfh.close()
log_path = outdir + 'log.txt'
prefix = 'NODE'
kingdom = 'Bacteria'
gcode = '11'
cmd = '%s --outdir %s --force --prefix %s %s --strain %s --kingdom %s --gcode %s --cpus 1 2>>%s' % (
        args.prokka, outdir, prefix, out_path, prefix, kingdom, gcode, log_path)
print('Now running Prokka: '+ cmd)
os.system(cmd)
os.system('rm ' + out_path)
os.system('mv ' + outdir + 'NODE.fna ' + out_path)
infile = outdir + 'NODE_tep.ptt'
gbfh = open(outdir + 'NODE.ptt', 'w')
os.system(args.perl + ' ' + args.gbptt + ' < ' + outdir + 'NODE.gbf > ' + infile)
infh = open(infile)
for line in infh:
    new_line = line.split('\n')[0].split('\t')
    if len(new_line) == 8:
        gbfh.write('\t'.join(new_line[:4]) + '\t')
        if new_line[4] != '-':
            gbfh.write(new_line[4])
        else:
            gbfh.write(new_line[5])
        gbfh.write('\t-\t' + '\t'.join(new_line[5:]) + '\n')
infh.close()
os.system('rm ' + infile)
gbfh.close()
