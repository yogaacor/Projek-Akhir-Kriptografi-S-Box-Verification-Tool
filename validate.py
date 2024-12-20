# validate.py
def validate_sbox(s_box):
    """Validasi apakah S-Box memiliki panjang 256 dan elemen unik."""
    if len(s_box) != 256:
        return False, "Panjang S-Box bukan 256."
    if len(set(s_box)) != 256:
        return False, "S-Box memiliki elemen duplikat."
    return True, "S-Box valid."
