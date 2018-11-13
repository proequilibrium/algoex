
seq_begining = 1
total=75000
seq_len=700

for file_num in range(int(total/seq_len)):
    with open('file-num{}--{}-{}.txt'.format(file_num, seq_begining, seq_begining+seq_len),'w') as file:
        file.write("cislo\n")
        for num in range(seq_len):
            file.write('{:06}\n'.format(seq_begining+num))
        print('soubor: {}'.format(seq_begining+seq_len-1))
    seq_begining = seq_begining + seq_len
