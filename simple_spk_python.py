def input_lokasi():
    print("\n--- INPUT DATA LOKASI ---")
    lokasi_list = []
    jumlah_lokasi = int(input("Masukkan jumlah lokasi: "))
    for i in range(jumlah_lokasi):
        nama = input(f"Nama lokasi #{i+1}: ")
        keterangan = input(f"Keterangan lokasi #{i+1}: ")
        lokasi_list.append({'nama': nama, 'keterangan': keterangan})
    return lokasi_list

def input_kriteria():
    print("\n--- INPUT DATA KRITERIA ---")
    kriteria_list = []
    jumlah_kriteria = int(input("Masukkan jumlah kriteria: "))
    for i in range(jumlah_kriteria):
        nama = input(f"Nama kriteria #{i+1}: ")
        kriteria_list.append({'nama': nama})
    return kriteria_list

def input_nilai_kriteria(lokasi_list, kriteria_list):
    print("\n--- INPUT NILAI KRITERIA BERDASARKAN KRITERIA ---")

    # Inisialisasi dictionary nilai kosong di setiap lokasi
    for lokasi in lokasi_list:
        lokasi['nilai'] = {}

    # Iterasi berdasarkan kriteria
    for kriteria in kriteria_list:
        print(f"\nMasukkan nilai untuk kriteria: {kriteria['nama']}")
        for lokasi in lokasi_list:
            while True:
                input_str = input(f"  - {lokasi['nama']} ({lokasi['keterangan']}) (0-100, kosong jika tidak ada): ").strip()
                if input_str == "":
                    lokasi['nilai'][kriteria['nama']] = None
                    break
                try:
                    nilai = float(input_str)
                    if 0 <= nilai <= 100:
                        lokasi['nilai'][kriteria['nama']] = nilai
                        break
                    else:
                        print("    Nilai harus antara 0 dan 100.")
                except ValueError:
                    print("    Input tidak valid. Masukkan angka atau kosong.")
    
    return lokasi_list

def input_bobot(kriteria_list, lokasi_list):
    print("\nMasukkan bobot untuk kriteria yang valid (yang nilainya lengkap untuk semua lokasi):")
    total_bobot = 0
    kriteria_valid = []

    for kriteria in kriteria_list:
        nama = kriteria['nama']
        # Cek apakah SEMUA lokasi memiliki nilai (tidak None)
        lengkap = all(lokasi['nilai'].get(nama) is not None for lokasi in lokasi_list)
        if lengkap:
            bobot = float(input(f"Bobot untuk kriteria '{nama}': "))
            kriteria['bobot'] = bobot
            total_bobot += bobot
            kriteria_valid.append(kriteria)
        else:
            print(f"Kriteria '{nama}' dilewati karena ada nilai yang kosong.")

    # Normalisasi bobot total = 1
    for kriteria in kriteria_valid:
        kriteria['bobot'] /= total_bobot

    return kriteria_valid

def hitung_smart(lokasi_list, kriteria_list):
    hasil = []
    for lokasi in lokasi_list:
        skor_total = 0
        for kriteria in kriteria_list:
            nama_kriteria = kriteria['nama']
            nilai = lokasi['nilai'].get(nama_kriteria)
            bobot = kriteria['bobot']
            if nilai is not None:
                skor_total += bobot * nilai
        hasil.append({
            'nama': lokasi['nama'],
            'keterangan': lokasi['keterangan'],
            'skor': skor_total
        })
    return sorted(hasil, key=lambda x: x['skor'], reverse=True)

def tampilkan_hasil(hasil):
    print("\n--- HASIL PERHITUNGAN SMART ---")
    for i, lokasi in enumerate(hasil, 1):
        print(f"{i}. {lokasi['nama']} ({lokasi['keterangan']}) - Skor: {lokasi['skor']:.2f}")

def main():
    lokasi_list = input_lokasi()
    kriteria_list = input_kriteria()
    lokasi_list = input_nilai_kriteria(lokasi_list, kriteria_list)
    kriteria_list_bobot = input_bobot(kriteria_list, lokasi_list)
    hasil = hitung_smart(lokasi_list, kriteria_list_bobot)
    tampilkan_hasil(hasil)
    
if __name__ == "__main__":
    main()
