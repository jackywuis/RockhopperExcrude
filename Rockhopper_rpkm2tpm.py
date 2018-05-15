import argparse

parser = argparse.ArgumentParser(description='This program is written to calculate TPM according to RPKM given by '
                                             'NC_999999_transcripts.txt given by Rockhopper. '
                                             '(Available from http://cs.wellesley.edu/~btjaden/Rockhopper/) \n'
                                             'The calculation is based on RPKM = TPM * 1000 * total number of '
                                             'transcripts sampled / (read length * total number of mapped reads) \n'
                                             'Usage: python Rockhopper_rpkm2tpm.py -i /path/of/input/ \n'
                                             'Output file with name transcripts.csv will include position information, '
                                             'length, strand direction, ene name, product, raw counts, normalized '
                                             'counts, RPKM, TPM, and expression counts')
parser.add_argument('-i', '--input', type=str, help='path of folder that contain target NC_999999_transcripts.txt and '
                                                    'summary.txt')
args = parser.parse_args()

outdir = args.input
if outdir.split('/')[-1] != '':
    outdir += '/'
su = [0, 0]
infh = open(outdir + 'summary.txt')
for line in infh:
    if 'Successfully aligned reads:' in line:
        su[0] += int(line.split('\t')[1])
    elif 'Number of predicted RNAs' in line:
        su[1] = int(line.split('\n')[0].split('\t')[-1])
infh.close()
infh = open(outdir + 'NC_999999_transcripts.txt')
oufh = open(outdir + 'transcripts.csv', 'w')
oufh.write('Start\tStop\tLength\tStrand\tName\tProduct\tRawCount\tNormalizedCount\tRPKM\tTPM\tExpression\n')
infh.next()
for line in infh:
    n = line.split('\n')[0].split('\t')
    if len(n) == 14:
        if (int(n[8]) + int(n[9]) != 0) and (((n[1] != '') and (n[2] != '')) or ((n[0] != '') and (n[3] != ''))):
            l = 1
            if (n[1] != '') and (n[2] != ''):
                l += abs(int(n[2]) - int(n[1]))
                oufh.write(n[1] + '\t' + n[2])
            elif (n[0] != '') and (n[3] != ''):
                l += abs(int(n[3]) - int(n[0]))
                oufh.write(n[0] + '\t' + n[3])
            oufh.write('\t' + str(l) + '\t' + n[4] + '\t')
            if n[5] != '-':
                oufh.write(n[5] + '\t' + n[7])
            elif n[7] != '-':
                oufh.write(n[7].split('antisense: ')[1] + '\t' + n[7])
            else:
                oufh.write(n[6] + '\t' + n[6])
            oufh.write('\t' + str(int(n[8]) + int(n[9])) + '\t' + str(int(n[10]) + int(n[11])) + '\t' + n[
                12] + '\t' + str(((3 * int(n[12]) * su[0]) / su[1]) / 20) + '\t' + n[13] + '\n')
oufh.close()
