# truth_table.py
import numpy as np

def truth_table(sbox, n, m):
    """Membuat tabel kebenaran untuk S-Box."""
    table = []
    for i in range(m):
        column = [(sbox[x] >> i) & 1 for x in range(2**n)]
        column = [2 * val - 1 for val in column]
        table.append(column)
    return np.array(table)
