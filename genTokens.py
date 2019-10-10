from tokenizer import readFile
import os
import sys

try:
    os.mkdir(os.getcwd()+'/results')
except:
    print("Directory already exist!!!")


read_file = sys.argv[1]
file = read_file.split('.')[0]
indexToWord, w2i_corpus4, totalTokens = readFile([read_file], flag=True)

f = open('data_structures/'+file+'_tokens.txt', 'r')
tokens = [x.split('\n')[0]for x in f.readlines()]
tokens.pop()
tokens.pop()
sentences = []
tsize = len(tokens)
i=0
while i<tsize:
    currSent = []
    while i<tsize and tokens[i] != "</$>":
        if tokens[i] != "<$>":
            currSent.append(tokens[i])
        i+=1
    sentences.append(' '.join(currSent))
    i+=1
f.close()
#os.remove('data_structures/'+file+'_tokens.txt')
f = open('results/'+file+'_tokens.txt', 'a+')
for sentence in sentences:
    f.write(sentence+'\n')
f.close()

