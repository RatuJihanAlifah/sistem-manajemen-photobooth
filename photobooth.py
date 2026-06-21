import csv
import os

FILE_BOOKING = "photobooth.csv"
FILE_BG = "background.csv"
FILE_PAKET = "paket.csv"

class PhotoBoothManager:
    def __init__(self):
        self.database_booking = {}
        self.antrean_foto = []
        self.list_background = []
        self.list_paket = {} 
        
        self.init_master_files()
        self.load_data()

    def init_master_files(self):
        if not os.path.exists(FILE_BG):
            with open(FILE_BG, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['nama_background'])
                
        if not os.path.exists(FILE_PAKET):
            with open(FILE_PAKET, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['nama_paket', 'harga'])

    def load_data(self):
        # Load Background
        self.list_background = []
        with open(FILE_BG, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.list_background.append(row['nama_background'])

        # Load Paket
        self.list_paket = {}
        with open(FILE_PAKET, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.list_paket[row['nama_paket'].lower()] = int(row['harga'])

        # Load Data Booking
        self.database_booking = {}
        self.antrean_foto = []
        if os.path.exists(FILE_BOOKING):
            with open(FILE_BOOKING, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.database_booking[row['id_booking']] = row
                    if row['status_antrean'] == 'Mengantre':
                        self.antrean_foto.append(row)

    def save_all(self):
        with open(FILE_BOOKING, mode='w', newline='') as f:
            fieldnames = ['id_booking', 'nama', 'email', 'background', 'paket', 'tambah_cetak', 'status_antrean']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for data in self.database_booking.values():
                writer.writerow(data)

        with open(FILE_BG, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nama_background'])
            for bg in self.list_background:
                writer.writerow([bg])

        with open(FILE_PAKET, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nama_paket', 'harga'])
            for nama, harga in self.list_paket.items():
                writer.writerow([nama.capitalize(), harga])

    # KELOLA SISTEM

    def menu_kelola_sistem(self):
        while True:
            print("\n--- [ KELOLA SISTEM ] ---")
            print("1. Kelola Background")
            print("2. Kelola Paket")
            print("3. Kembali ke Menu Utama")
            pilih = input("Pilih menu (1-3): ")
            
            if pilih == '1':
                print("\n>> KELOLA BACKGROUND <<")
                print("Background saat ini:")
                for idx, bg in enumerate(self.list_background, 1):
                    print(f"   {idx}. {bg}")
                print("\nAksi: [1] Tambah Background  [2] Hapus Background  [3] Kembali")
                aksi = input("Pilih aksi: ")
                if aksi == '1':
                    baru = input("Masukkan nama background baru: ").strip()
                    if baru and baru not in self.list_background:
                        self.list_background.append(baru)
                        self.save_all()
                        print(f"Background '{baru}' berhasil ditambahkan!")
                    else:
                        print("Nama kosong atau sudah ada.")
                elif aksi == '2':
                    hps = int(input("Masukkan nomor background yang mau dihapus: ")) - 1
                    if 0 <= hps < len(self.list_background):
                        removed = self.list_background.pop(hps)
                        self.save_all()
                        print(f"Background '{removed}' berhasil dihapus.")
                    else:
                        print("Nomor tidak valid.")
                        
            elif pilih == '2':
                print("\n>> KELOLA PAKET <<")
                print("Paket saat ini:")
                paket_keys = list(self.list_paket.keys())
                for idx, pkt in enumerate(paket_keys, 1):
                    print(f"   {idx}. {pkt.capitalize()} - Rp {self.list_paket[pkt]:,}")
                print("\nAksi: [1] Tambah/Update Paket  [2] Hapus Paket  [3] Kembali")
                aksi = input("Pilih aksi: ")
                if aksi == '1':
                    nama_p = input("Nama paket: ").strip().lower()
                    harga_p = int(input("Harga paket (angka saja): "))
                    self.list_paket[nama_p] = harga_p
                    self.save_all()
                    print(f"Paket '{nama_p.capitalize()}' berhasil disimpan!")
                elif aksi == '2':
                    hps = int(input("Masukkan nomor paket yang mau dihapus: ")) - 1
                    if 0 <= hps < len(paket_keys):
                        del self.list_paket[paket_keys[hps]]
                        self.save_all()
                        print("Paket berhasil dihapus.")
                    else:
                        print("Nomor tidak valid.")
            elif pilih == '3':
                break

    # KELOLA BOOKING

    def menu_kelola_booking(self):
        while True:
            print("\n--- [ KELOLA BOOKING ] ---")
            print("1. Booking Photobooth")
            print("2. Lihat Booking")
            print("3. Cari Booking")
            print("4. Urutkan Booking")
            print("5. Update Booking")
            print("6. Hapus Booking")
            print("7. Lihat Antrian")
            print("8. Panggil Antrian")
            print("9. Total Pendapatan")
            print("10. Kembali ke Menu Utama")
            pilih = input("Pilih menu : ")

            if pilih == '1':
                print("\n--- 1. BOOKING PHOTOBOOTH ---")
                id_booking = input("Masukkan ID Booking: ").strip()
                if id_booking in self.database_booking:
                    print(" ID Booking sudah terdaftar!"); continue
                nama = input("Nama Pelanggan: ")
                email = input("Email: ")
                
                print("\nPilihan Background:")
                for idx, bg in enumerate(self.list_background, 1): print(f"{idx}. {bg}")
                pilih_bg = int(input("Pilih nomor background: ")) - 1
                
                print("\nPilihan Paket:")
                paket_keys = list(self.list_paket.keys())
                for idx, pkt in enumerate(paket_keys, 1): print(f"{idx}. {pkt.capitalize()} (Rp {self.list_paket[pkt]:,})")
                pilih_pkt = int(input("Pilih nomor paket: ")) - 1
                
                cetak = input("Tambah Cetak? (+Rp 20,000) (Y/N): ").upper()
                
                data = {
                    'id_booking': id_booking, 'nama': nama, 'email': email,
                    'background': self.list_background[pilih_bg], 'paket': paket_keys[pilih_pkt].capitalize(),
                    'tambah_cetak': cetak, 'status_antrean': 'Mengantre'
                }
                self.database_booking[id_booking] = data
                self.antrean_foto.append(data)
                self.save_all()
                print(f"Booking sukses untuk {nama}!")

            elif pilih == '2':
                print("\n--- 2. DAFTAR MASTER BOOKING ---")
                if not self.database_booking: print("Belum ada data."); continue
                for b_id, d in self.database_booking.items():
                    print(f"ID: {b_id} | Nama: {d['nama']} | Paket: {d['paket']} | Status: {d['status_antrean']}")

            elif pilih == '3':
                print("\n--- 3. CARI BOOKING (HASH MAP LOOKUP) ---")
                id_cari = input("Masukkan ID Booking: ").strip()
                if id_cari in self.database_booking:
                    b = self.database_booking[id_cari]
                    print(f"\n Ketemu!\nNama: {b['nama']}\nPaket: {b['paket']}\nBackground: {b['background']}")
                else: print("Data tidak ditemukan.")

            elif pilih == '4':
                print("\n--- 4. URUTKAN BOOKING (BUBBLE SORT BY NAMA) ---")
                df = list(self.database_booking.values())
                n = len(df)
                for i in range(n):
                    for j in range(0, n-i-1):
                        if df[j]['nama'].lower() > df[j+1]['nama'].lower():
                            df[j], df[j+1] = df[j+1], df[j]
                for d in df: print(f"Nama: {d['nama']} | ID: {d['id_booking']}")

            elif pilih == '5':
                print("\n--- 5. UPDATE BACKGROUND BOOKING ---")
                id_up = input("Masukkan ID Booking: ").strip()
                if id_up in self.database_booking:
                    for idx, bg in enumerate(self.list_background, 1): print(f"{idx}. {bg}")
                    pilih_bg = int(input("Pilih nomor background baru: ")) - 1
                    self.database_booking[id_up]['background'] = self.list_background[pilih_bg]
                    self.save_all()
                    print("Background berhasil diubah!")
                else: print("ID tidak ditemukan.")

            elif pilih == '6':
                print("\n--- 6. HAPUS BOOKING ---")
                id_hps = input("Masukkan ID Booking yang mau dihapus: ").strip()
                if id_hps in self.database_booking:
                    del self.database_booking[id_hps]
                    self.antrean_foto = [b for b in self.antrean_foto if b['id_booking'] != id_hps]
                    self.save_all()
                    print("Data dihapus dari database.")
                else: print("ID tidak ditemukan.")

            elif pilih == '7':
                print("\n--- 7. ANTREAN FOTO HARI INI (QUEUE FIFO) ---")
                if not self.antrean_foto: print("Antrean kosong."); continue
                for idx, ant in enumerate(self.antrean_foto, 1):
                    print(f"Antrean {idx}. [{ant['id_booking']}] {ant['nama']}")

            elif pilih == '8':
                print("\n--- 8. PANGGIL ANTREAN BERIKUTNYA ---")
                if not self.antrean_foto: print("Tidak ada antrean."); continue
                dipanggil = self.antrean_foto.pop(0) # FIFO Dequeue
                self.database_booking[dipanggil['id_booking']]['status_antrean'] = 'Selesai Foto'
                self.save_all()
                print(f"📢 Silakan masuk studio: {dipanggil['nama']} (ID: {dipanggil['id_booking']})!")

            elif pilih == '9':
                print("\n--- 9. TOTAL PENDAPATAN ---")
                total = 0
                for b in self.database_booking.values():
                    nama_pkt = b['paket'].lower()
                    if nama_pkt in self.list_paket: total += self.list_paket[nama_pkt]
                    if b['tambah_cetak'].upper() == 'Y': total += 20000
                print(f"💰 Total Pendapatan Studio: Rp {total:,}")

            elif pilih == '10':
                break

# --- MENU UTAMA WINDOW ---
def main():
    app = PhotoBoothManager()
    while True:
        print("\n=====================================")
        print("    SISTEM MANAJEMEN PHOTOBOOTH      ")
        print("=====================================")
        print("1. Kelola Sistem (Background & Paket)")
        print("2. Kelola Booking")
        print("3. Keluar")
        print("=====================================")
        
        pilihan = input("Pilih menu utama (1-3): ")
        if pilihan == '1':
            app.menu_kelola_sistem()
        elif pilihan == '2':
            app.menu_kelola_booking()
        elif pilihan == '3':
            print("Menutup aplikasi. Terima kasih!")
            break
        else:
            print("Pilihan menu salah!")

if __name__ == "__main__":
    main()