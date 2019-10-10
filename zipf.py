import numpy as np
import matplotlib.pyplot as plt
from math import log10

def draw_zipf(freq):
    reverse_sorted_freq = []

    for t in freq.keys():
        if t!='1' and t!='2':
            reverse_sorted_freq.append(freq[t])

    reverse_sorted_freq.sort(reverse=True)
    reverse_sorted_freq = reverse_sorted_freq[20000:25000]

    rank = range(1, len(reverse_sorted_freq)+1)
    #rank=rank[10001:11000]

    plt.plot(rank, reverse_sorted_freq)
    plt.pause(5)

if __name__ == "__main__":
    count1 = np.load('data_structures/corpus2_count_1.npy').item()
    draw_zipf(count1)