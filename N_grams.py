from tokenizer import readFile
from tokenizer import tokenize
from math import log
import numpy as np
import sys
from itertools import islice
import os
from tokenizer import generate_ngrams

tokenReadSize = 31457280
d = 0.75

try:
    os.mkdir(os.getcwd()+'/data_structures')
except:
    print("Directory already exist!!!")

read_file = 'corpus2.txt'
fileName = read_file.split('.')[0]
indexToWord, wordToIndex, totalTokens = readFile([read_file], False)

np.save('data_structures/'+fileName+'_w2i.npy', wordToIndex)

def prepare_counts(tokens, n, corpus_name):
    i = 0
    while i<n:
        gram_count = {}
        gram_data = generate_ngrams(tokens, i+1)
        print('grams_generated...')
        total_grams = len(gram_data)
        for j in range(total_grams):
            gram = gram_data[j]
            if gram in gram_count.keys():
                gram_count[gram] += 1
            else:
                gram_count[gram] = 1
        
        np.save('data_structures/'+corpus_name+'_count_'+str(i+1)+'.npy', gram_count)
        del(gram_count)
        
        gram_preceeding = {}
        gram_data = generate_ngrams(tokens, i+1)
        total_grams = len(gram_data)
        for j in range(total_grams):
            gram = gram_data[j]
            if gram not in gram_preceeding.keys():
                gram_preceeding[gram] = set()
            if j<total_grams-1:
                gram_preceeding[gram].add(gram_data[j+1].split(' ')[-1])
        
        np.save('data_structures/'+corpus_name+'_preceeding_'+str(i+1)+'.npy', gram_preceeding)
        del(gram_preceeding)
        
        gram_succeeding = {}
        gram_data = generate_ngrams(tokens, i+1)
        total_grams = len(gram_data)
        for j in range(total_grams):
            gram = gram_data[j]
            if gram not in gram_succeeding.keys():
                gram_succeeding[gram] = set()
            if j>0:
                gram_succeeding[gram].add(gram_data[j-1].split(' ')[0])
        
        np.save('data_structures/'+corpus_name+'_succeeding_'+str(i+1)+'.npy', gram_succeeding)
        del(gram_succeeding)
        del(gram_data)
        i+=1


f = open('data_structures/tokens.txt','r')
f_new = open('data_structures/'+fileName+'_new_tokens.txt', 'a+')
chunk = f.readlines(54857600)
chunk = [x.split('\n')[0] for x in chunk]
while len(chunk)>0:
    res = []
    for x in chunk:
        if x in wordToIndex.keys():
           res.append(str(wordToIndex[x]))
        elif x=="</$><$>":
            res.append(str(wordToIndex["</$>"]))
            res.append(str(wordToIndex["<$>"]))
        elif x=="<$></$>":
            res.append(str(wordToIndex["<$>"]))
            res.append(str(wordToIndex["</$>"]))
    st = '\n'.join(res)
    f_new.write(st)
    chunk = f.readlines(54857600)
    chunk = [x.split('\n')[0] for x in chunk]
f.close()
f_new.close()
del(wordToIndex)
del chunk[:]

f = open('data_structures/'+fileName+'_new_tokens.txt', 'r')
currToken = [x.split('\n')[0] for x in f.readlines(tokenReadSize)]
if currToken[-1] != "2":
    x = f.readline().split('\n')[0]
    while x != "2" and x:
        currToken.append(x)
        x = f.readline().split('\n')[0]
    currToken.append("2")
prepare_counts(currToken, 6, fileName)
del(currToken)
f.close()