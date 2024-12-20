# validate.py
# Fungsi melakukan validasi terhadap S-Box 
def validate_sbox(s_box):
    if len(s_box) != 256:
        return False, 
    if len(set(s_box)) != 256:
        return False, 
    return True, 
