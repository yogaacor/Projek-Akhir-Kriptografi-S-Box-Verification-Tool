import streamlit as st
import pandas as pd
from io import BytesIO
from validate import validate_sbox
from metrics import nonlinearity, sac, bic_nl, bic_sac, lap, dap

# Sidebar untuk informasi anggota kelompok
st.sidebar.header("Informasi Anggota Kelompok")
st.sidebar.write("""
- Nama Anggota 1: Yoga Yudha Tama (4611422079)
- Nama Anggota 2: Thoriq Ibrahim Farras (4611422074)
- Nama Anggota 3: Hamza Pratama (4611422068)
- Nama Anggota 4: Lintang Isnandar (4611422061)
""")

st.title("S-Box Verification Tool")

st.write("Ketentuan Tugas Projek")
st.write("""
- **NonLinearity (NL)** mencapai nilai: **112**
- **Strict Avalanche Criterion (SAC)** mencapai nilai: **0.50073**
- **Bit Independence Criterion-NonLinearity (BIC-NL)** mencapai nilai: **112**
- **Bit Independence Criterion-Strict Avalanche Criterion (BIC-SAC)** mencapai nilai: **0.50237**
- **Linear Approximation Probability (LAP)** mencapai nilai: **0.0625**
- **Differential Approximation Probability (DAP)** mencapai nilai: **0.015625**
""")

# Unggah File
uploaded_file = st.file_uploader("Upload File S-Box (Excel)", type=["xlsx"])

if uploaded_file:
    # Coba membaca file Excel dan menangani kesalahan jika ada
    try:
        sbox_df = pd.read_excel(uploaded_file, sheet_name=0, header=None)
        sbox_values = sbox_df.values.flatten().tolist()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

    # Menampilkan data S-Box
    st.write("Data S-Box yang diunggah:")
    st.dataframe(sbox_df)

    # Validasi S-Box
    is_valid, validation_message = validate_sbox(sbox_values)
    if not is_valid:
        st.error(validation_message)
    else:
        st.success(validation_message)

        # Pilihan Operasi
        operations = {
            "Nonlinearity (NL)": lambda: nonlinearity(sbox_values, 8, 8),
            "Strict Avalanche Criterion (SAC)": lambda: sac(sbox_values, 8),
            "Bit Independence Criterion - NL (BIC-NL)": lambda: bic_nl(sbox_values, 8),
            "Bit Independence Criterion - SAC (BIC-SAC)": lambda: bic_sac(sbox_values),
            "Linear Approximation Probability (LAP)": lambda: lap(sbox_values, 8),
            "Differential Approximation Probability (DAP)": lambda: dap(sbox_values, 8),
        }

        # Pilih operasi
        selected_operations = st.multiselect("Pilih Operasi", operations.keys())
        
        # Validasi pilihan operasi
        if not selected_operations:
            st.warning("Tidak ada operasi yang dipilih. Silakan pilih operasi yang diinginkan.")

        # Jalankan Operasi
        if st.button("Jalankan Operasi"):
            results = {}
            for op, func in operations.items():
                if op in selected_operations:
                    result = func()
                    if result is not None:  # Pastikan operasi mengembalikan nilai
                        results[op] = result
                    else:
                        st.warning(f"Hasil untuk operasi {op} tidak tersedia.")

            if results:
                st.write("Hasil Operasi:")
                st.json(results)

                # Unduh Hasil Sebagai Excel
                results_df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])

                # Simpan hasil ke file Excel menggunakan BytesIO
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                    results_df.to_excel(writer, index=False, sheet_name="S-Box Results")
                excel_data = excel_buffer.getvalue()

                st.download_button(
                    label="Download Hasil (Excel)",
                    data=excel_data,
                    file_name="hasil_sbox.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.warning("Tidak ada hasil untuk ditampilkan.")
