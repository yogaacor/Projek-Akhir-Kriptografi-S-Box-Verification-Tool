# metrics.py
import numpy as np
from truth_table import truth_table
from utils import walsh_transform, hamming_weight

def nonlinearity(sbox, n, m):
    table = truth_table(sbox, n, m)
    min_distance = float('inf')
    for column in table:
        W = walsh_transform(column)
        max_walsh = np.max(np.abs(W))
        distance = 2**(n - 1) - max_walsh / 2
        min_distance = min(min_distance, distance)
    return int(min_distance)

def sac(sbox, n):
    total = 0
    for i in range(2**n):
        original = sbox[i]
        for bit in range(n):
            flipped_input = i ^ (1 << bit)
            flipped_output = sbox[flipped_input]
            diff = original ^ flipped_output
            total += hamming_weight(diff)
    return total / (n * 2**n * n)

def bic_nl(sbox, n):
    total_nl = 0
    count = 0
    for bit1 in range(n):
        for bit2 in range(bit1 + 1, n):
            count += 1
            sbox_bit1 = [(x >> bit1) & 1 for x in sbox]
            sbox_bit2 = [(x >> bit2) & 1 for x in sbox]
            combined = [2 * (b1 ^ b2) - 1 for b1, b2 in zip(sbox_bit1, sbox_bit2)]
            W = walsh_transform(combined)
            max_walsh = np.max(np.abs(W))
            total_nl += 2**(n - 1) - max_walsh / 2
    return int(total_nl / count)

def bic_sac(sbox):
    n = len(sbox)
    bit_length = 8
    total_pairs = 0
    total_independence = 0

    for i in range(bit_length):
        for j in range(i + 1, bit_length):
            independence_sum = 0
            for x in range(n):
                y1 = sbox[x]
                for bit_to_flip in range(bit_length):
                    flipped_x = x ^ (1 << bit_to_flip)
                    y2 = sbox[flipped_x]
                    independence_sum += (
                        ((y1 >> i) & 1 ^ (y2 >> i) & 1) ^
                        ((y1 >> j) & 1 ^ (y2 >> j) & 1)
                    )
            total_independence += independence_sum / (n * bit_length)
            total_pairs += 1
    return total_independence / total_pairs

def lap(sbox, n):
    max_bias = 0
    for a in range(1, 2**n):
        for b in range(1, 2**n):
            bias = 0
            for x in range(2**n):
                input_parity = hamming_weight(x & a) % 2
                output_parity = hamming_weight(sbox[x] & b) % 2
                if input_parity == output_parity:
                    bias += 1
            bias = abs(bias - 2**(n - 1))
            max_bias = max(max_bias, bias / 2**n)
    return max_bias

def dap(sbox, n):
    max_diff_prob = 0
    for dx in range(1, 2**n):
        for dy in range(1, 2**n):
            count = 0
            for x in range(2**n):
                if sbox[x ^ dx] ^ sbox[x] == dy:
                    count += 1
            prob = count / 2**n
            max_diff_prob = max(max_diff_prob, prob)
    return max_diff_prob
