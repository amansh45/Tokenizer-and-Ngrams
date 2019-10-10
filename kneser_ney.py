from tokenizer import generate_ngrams, tokenize
from math import log
import numpy as np
import os

d = 0.75

def findcount(gram, corpus_name):
    gram_size = len(gram.split(' '))
    file_name = corpus_name+'_count_'+str(gram_size)+'.npy'
    gram_count = np.load('data_structures/'+file_name).item()
    if gram in gram_count.keys():
        return gram_count[gram]
    else:
        return 0

def perplexity(prob, nwords):
    return pow((1.0/prob), 1.0/nwords)


def findSucc(gram, corpus_name):
    gram_size = len(gram.split(' '))
    file_name = corpus_name+'_preceeding_'+str(gram_size)+'.npy'
    gram_preceeding = np.load('data_structures/'+file_name).item()
    if gram in gram_preceeding.keys():
        return len(gram_preceeding[gram])
    else:
        return 0

def findPre(gram, corpus_name):
    gram_size = len(gram.split(' '))
    file_name = corpus_name+'_succeeding_'+str(gram_size)+'.npy'
    gram_succeeding = np.load('data_structures/'+file_name).item()
    if gram in gram_succeeding.keys():
        return len(gram_succeeding[gram])
    else:
        return 0

def total_unigrams(corpus_name):
    file_name = corpus_name+'_count_1.npy'
    gram_count = np.load('data_structures/'+file_name).item()
    unigrams = 0.0
    for x in gram_count:
        unigrams += gram_count[x] 
    return unigrams
    
def kneser_ney(gram, corpus, highestOrder):
    global total_unigrams
    gram_size = len(gram.split(' '))    
    first_term = 0.0
    lamda = 0.75
    gram_splitted = gram.split(' ')
    
    g_count_gram = findcount(gram, corpus)
    print('1')
    if gram_size == 1:
        first_term += max(g_count_gram-d, 0)
        first_term /= total_unigrams(corpus)
        return first_term
    
    send_gram = ' '.join(gram_splitted[1:gram_size])
    second_gram = ' '.join(gram_splitted[0:gram_size-1])
    
    g_count_sgram = findcount(second_gram, corpus)
    g_succ_gram = findSucc(gram, corpus)
    g_succ_sgram = findSucc(second_gram, corpus)
    g_pre_sgram = findPre(second_gram, corpus)
    if highestOrder:
        first_term += max(g_count_gram-d, 0)
        if g_count_sgram == 0:
            first_term = 0
            lamda = 0.75
        else:
            first_term /= g_count_sgram
            lamda /= g_count_sgram
    else:
        first_term += max(g_succ_gram-d, 0)
        if g_succ_sgram == 0:
            first_term = 0
            lamda = 0.75
        else:            
            first_term /= g_succ_sgram
            lamda /= g_succ_sgram
    
    if g_pre_sgram != 0:
        lamda *= g_pre_sgram

    return first_term + (lamda * kneser_ney(send_gram, corpus, False))

def kneserNeySmoothing(tokenized_sent, corpus, gram_count):
    tokenized_sent.pop()
    tokenized_sent.pop()
    sent_grams = generate_ngrams(tokenized_sent, gram_count)
    sent_grams.pop()
    curr_prob = 0.0
    for gram in sent_grams:
        res = kneser_ney(gram, corpus, True)
        if res != 0:
            curr_prob = curr_prob + log(res)
        curr_prob = curr_prob + log(abs())
    return curr_prob

try:
    os.mkdir(os.getcwd()+'/results')
except:
    print("Directory already exist!!!")

perp_corpus3_t1_6 = []
perp_corpus3_t1_4 = []
perp_corpus3_t2_6 = []
perp_corpus3_t2_4 = []
perp_corpus4_t1_6 = []
perp_corpus4_t1_4 = []
perp_corpus4_t2_6 = []
perp_corpus4_t2_4 = []
roll_number = '2018201084'
f1 = open('results/'+roll_number+'-LM1-corpus3-perplexity.txt','a+')
f2 = open('results/'+roll_number+'-LM2-corpus3-perplexity.txt','a+')
f3 = open('results/'+roll_number+'-LM3-corpus3-perplexity.txt','a+')
f4 = open('results/'+roll_number+'-LM4-corpus3-perplexity.txt','a+')
f5 = open('results/'+roll_number+'-LM1-corpus4-perplexity.txt','a+')
f6 = open('results/'+roll_number+'-LM2-corpus4-perplexity.txt','a+')
f7 = open('results/'+roll_number+'-LM3-corpus4-perplexity.txt','a+')
f8 = open('results/'+roll_number+'-LM4-corpus4-perplexity.txt','a+')

probs = {'corpus3': {'LM1': [], 'LM2': [], 'LM3': [], 'LM4': []}, 'corpus4': {'LM1': [], 'LM2': [], 'LM3': [], 'LM4': []}}
f = open('corpus3.txt', 'r')
sentence = f.readline()
nsentences = 0
while sentence:
    tokenized_sent = tokenize(sentence, False)
    a, b, c, d = kneserNeySmoothing(tokenized_sent, 'corpus1', 4), kneserNeySmoothing(tokenized_sent, 'corpus1', 6), kneserNeySmoothing(tokenized_sent, 'corpus2', 4), kneserNeySmoothing(tokenized_sent, 'corpus2', 6)
    probs['corpus3']['LM1'].append(a)
    probs['corpus3']['LM2'].append(b)
    probs['corpus3']['LM3'].append(c)
    probs['corpus3']['LM4'].append(d)
    p = perplexity(a, len(tokenized_sent))
    q = perplexity(b, len(tokenized_sent))
    r = perplexity(c, len(tokenized_sent))
    s = perplexity(d, len(tokenized_sent))
    perp_corpus3_t1_4.append(p)
    perp_corpus3_t1_6.append(q)
    perp_corpus3_t2_4.append(r)
    perp_corpus3_t2_6.append(s)
    f1.write(sentence+'\t'+str(p)+'\n')
    f2.write(sentence+'\t'+str(q)+'\n')
    f3.write(sentence+'\t'+str(r)+'\n')
    f4.write(sentence+'\t'+str(s)+'\n')
    sentence = f.readline()
    nsentences+=1
f.close()
f1.write('\n'+str(sum(perp_corpus3_t1_4)/nsentences))
f1.close()
f2.write('\n'+str(sum(perp_corpus3_t1_6)/nsentences))
f2.close()
f3.write('\n'+str(sum(perp_corpus3_t2_4)/nsentences))
f3.close()
f4.write('\n'+str(sum(perp_corpus3_t2_6)/nsentences))
f4.close()
f = open('corpus4.txt', 'r')
sentence = f.readline()
nsentences = 0
while sentence:
    tokenized_sent = tokenize(sentence, False)
    a, b, c, d = kneserNeySmoothing(tokenized_sent, 'corpus1', 6), kneserNeySmoothing(tokenized_sent, 'corpus1', 4), kneserNeySmoothing(tokenized_sent, 'corpus2', 6), kneserNeySmoothing(tokenized_sent, 'corpus2', 4)
    probs['corpus4']['LM1'].append(a)
    probs['corpus4']['LM2'].append(b)
    probs['corpus4']['LM3'].append(c)
    probs['corpus4']['LM4'].append(d)
    p = perplexity(a, len(tokenized_sent))
    q = perplexity(b, len(tokenized_sent))
    r = perplexity(c, len(tokenized_sent))
    s = perplexity(d, len(tokenized_sent))
    perp_corpus4_t1_4.append(p)
    perp_corpus4_t1_6.append(q)
    perp_corpus4_t2_4.append(r)
    perp_corpus4_t2_6.append(s)
    f5.write(sentence+'\t'+str(p)+'\n')
    f6.write(sentence+'\t'+str(q)+'\n')
    f7.write(sentence+'\t'+str(r)+'\n')
    f8.write(sentence+'\t'+str(s)+'\n')
    sentence = f.readline()
    nsentences+=1
f.close()
f5.write('\n'+str(sum(perp_corpus4_t1_4)/nsentences))
f5.close()
f6.write('\n'+str(sum(perp_corpus4_t1_6)/nsentences))
f6.close()
f7.write('\n'+str(sum(perp_corpus4_t2_4)/nsentences))
f7.close()
f8.write('\n'+str(sum(perp_corpus4_t2_6)/nsentences))
f8.close()

np.save('results/probabilities.npy', probs)
