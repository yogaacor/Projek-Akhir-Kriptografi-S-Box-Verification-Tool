# validate.py
# Fungsi melakukan validasi terhadap S-Box
def validate_sbox(s_box):
    if len(s_box) != 256:
        return False, "S-Box harus memiliki 256 elemen."
    if len(set(s_box)) != 256:
        return False, "Semua elemen dalam S-Box harus unik."
    if any(val < 0 or val > 255 for val in s_box):
        return False, "Nilai dalam S-Box harus berada di antara 0 dan 255."
    return True, "S-Box valid."
