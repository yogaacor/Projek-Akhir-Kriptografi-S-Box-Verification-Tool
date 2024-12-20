# utils.py
import numpy as np

def hamming_weight(x):
    """Menghitung berat Hamming dari bilangan."""
    return bin(x).count('1')

def walsh_transform(column):
    """Melakukan Walsh Transform pada sebuah kolom."""
    n = len(column)
    W = np.array(column)
    for i in range(int(np.log2(n))):
        half = 2**i
        for j in range(0, n, 2 * half):
            for k in range(half):
                a = W[j + k]
                b = W[j + k + half]
                W[j + k] = a + b
                W[j + k + half] = a - b
    return W
