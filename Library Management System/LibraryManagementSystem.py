import tkinter as tk

class Kutuphane:
    def __init__(self, dosya_adi):
        self.dosya_adi = dosya_adi
        self.dosya = None

        try:
            self.dosya = open(self.dosya_adi, "a+")
        except FileNotFoundError:
            print(f"{self.dosya_adi} dosyası bulunamadı.")
        except Exception as e:
            print(f"Dosya açılırken bir hata oluştu: {e}")

    def __del__(self):
        if self.dosya:
            self.dosya.close()
            print(f"{self.dosya_adi} dosyası kapatıldı.")

    def ListBooks(self):
        if self.dosya:
            self.dosya.seek(0)  # Dosyanın başına git
            kitaplar = self.dosya.read().splitlines()  # Tüm satırları oku ve satırları ayır
            return kitaplar
        else:
            print("Dosya açık değil.")


    def AddBook(self, kitap_adi, yazar, yayin_yili, sayfa_sayisi):
        if self.dosya:
            yeni_kitap = f"{kitap_adi}, {yazar}, {yayin_yili}, {sayfa_sayisi}\n"
            self.dosya.write(yeni_kitap)
            print(f"{kitap_adi} kitabı başarıyla eklendi.")
        else:
            print("Dosya açık değil.")

    def RemoveBook(self, kitap_adi):
        if self.dosya:
            kitaplar = self.ListBooks()

            with open(self.dosya_adi, "w") as dosya:
                for kitap in kitaplar:
                    if kitap.split(',')[0].strip() != kitap_adi:
                        dosya.write(kitap + '\n')
                print(f"{kitap_adi} kitabı başarıyla silindi.")
        else:
            print("Dosya açık değil.")

class KutuphaneArayuzu:
    def __init__(self, pencere):
        self.pencere = pencere
        pencere.title("Kütüphane Uygulaması")
        pencere.geometry("350x250")

        self.kutuphane = Kutuphane("books.txt")

        self.etiket = tk.Label(pencere, text="Hoş geldiniz!")
        self.etiket.pack(pady=10)

        self.listele_buton = tk.Button(pencere, text="Kitapları Listeleyin", command=self.kitaplari_listele)
        self.listele_buton.pack(pady=5)

        self.ekle_buton = tk.Button(pencere, text="Kitap Ekle", command=self.kitap_ekle)
        self.ekle_buton.pack(pady=5)

        self.kaldir_buton = tk.Button(pencere, text="Kitabı Kaldır", command=self.kitap_kaldir)
        self.kaldir_buton.pack(pady=5)

        self.cikis_buton = tk.Button(pencere, text="Çıkış", command=pencere.quit)
        self.cikis_buton.pack(pady=5)

    def kitaplari_listele(self):
        kitaplar = self.kutuphane.ListBooks()
        if kitaplar:
            kitap_listesi = "\n".join(kitaplar)
            self.etiket.config(text=kitap_listesi)
        else:
            self.etiket.config(text="Kitap bulunamadı.")
        

    def kitap_ekle(self):
        self.ekle_penceresi = tk.Toplevel(self.pencere)
        self.ekle_penceresi.title("Kitap Ekle")
        self.ekle_penceresi.geometry("300x250")

        self.kitap_adi_etiket = tk.Label(self.ekle_penceresi, text="Kitap Adı:")
        self.kitap_adi_etiket.pack()
        self.kitap_adi_entry = tk.Entry(self.ekle_penceresi)
        self.kitap_adi_entry.pack(pady=5)

        self.yazar_etiket = tk.Label(self.ekle_penceresi, text="Yazar:")
        self.yazar_etiket.pack()
        self.yazar_entry = tk.Entry(self.ekle_penceresi)
        self.yazar_entry.pack(pady=5)

        self.yayin_yili_etiket = tk.Label(self.ekle_penceresi, text="Yayın Yılı:")
        self.yayin_yili_etiket.pack()
        self.yayin_yili_entry = tk.Entry(self.ekle_penceresi)
        self.yayin_yili_entry.pack(pady=5)

        self.sayfa_sayisi_etiket = tk.Label(self.ekle_penceresi, text="Sayfa Sayısı:")
        self.sayfa_sayisi_etiket.pack()
        self.sayfa_sayisi_entry = tk.Entry(self.ekle_penceresi)
        self.sayfa_sayisi_entry.pack(pady=5)

        self.ekle_buton = tk.Button(self.ekle_penceresi, text="Kitap Ekle", command=self.kitap_ekle_onayla)
        self.ekle_buton.pack()

    def kitap_ekle_onayla(self):
        kitap_adi = self.kitap_adi_entry.get()
        yazar = self.yazar_entry.get()
        yayin_yili = self.yayin_yili_entry.get()
        sayfa_sayisi = self.sayfa_sayisi_entry.get()

        self.kutuphane.AddBook(kitap_adi, yazar, yayin_yili, sayfa_sayisi)
        self.ekle_penceresi.destroy()

    def kitap_kaldir(self):
        self.kaldir_penceresi = tk.Toplevel(self.pencere)
        self.kaldir_penceresi.title("Kitap Kaldır")
        self.kaldir_penceresi.geometry("300x150")

        self.kitap_adi_etiket = tk.Label(self.kaldir_penceresi, text="Silmek İstediğiniz Kitabın Adı:")
        self.kitap_adi_etiket.pack()
        self.kitap_adi_entry = tk.Entry(self.kaldir_penceresi)
        self.kitap_adi_entry.pack(pady=5)

        self.kaldir_buton = tk.Button(self.kaldir_penceresi, text="Kitabı Kaldır", command=self.kitap_kaldir_onayla)
        self.kaldir_buton.pack()

    def kitap_kaldir_onayla(self):
        kitap_adi = self.kitap_adi_entry.get()
        self.kutuphane.RemoveBook(kitap_adi)
        self.kaldir_penceresi.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = KutuphaneArayuzu(root)
    root.mainloop()