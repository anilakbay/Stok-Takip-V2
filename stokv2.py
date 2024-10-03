import tkinter as tk
from tkinter import ttk
import sqlite3

class InventoryTrackingApplication:
    def __init__(self, root):
        #ana pencereyi oluştur  #root: tasarım alanını ifade ediyor!
        self.root = root        #self: tasarım alanına bağlanmayı sağlıyor!
        self.root.title("Inventory Tracking Application") #uygulama başlığı

        #veritabanı baglantısını oluştur!
        #gerekli tabloları oluştur!
        self.conn = sqlite3.connect('stock_tracking.db') # SQLite veritabanına bağlanılır.

        self.cursor = self.conn.cursor() # veritabanı bağlantısını (self.conn) kullanarak bir imleç (cursor) oluşturur. 
                                         # İmleç, SQL sorgularını çalıştırmak ve veritabanı ile etkileşimde bulunmak için kullanılır.
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS stocks(                            
                            id TEXT PRIMARY KEY,
                            urun_adi TEXT,
                            adet INTEGER,
                            birim_fiyati REAL,
                            toplam_deger REAL                           
                        )                                
        """)  # tablonun oluşturuılması
        self.conn.commit() #veritabanına bağlan ve değişiklikleri kaydet!

        #Giriş Alanları
        self.id_label = tk.Label(root, text="ID:")
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=0, column=1)

        #ürün adı etiketi ve giriş kutusu
        self.urun_adi_label = tk.Label(root, text="Ürün Adı:")
        self.urun_adi_label.grid(row=1, column=0)
        self.urun_adi_entry = tk.Entry(root)
        self.urun_adi_entry.grid(row=1, column=1)

        #adet etiketi ve giriş kutusu
        self.adet_label = tk.Label(root, text="Adet:")
        self.adet_label.grid(row=2, column=0)
        self.adet_entry = tk.Entry(root)
        self.adet_entry.grid(row=2, column=1)

        #birim fiyatı etiketi ve giriş kutusu
        self.birim_fiyati_label = tk.Label(root, text="Birim Fiyatı:")
        self.birim_fiyati_label.grid(row=3, column=0)
        self.birim_fiyati_entry = tk.Entry(root)
        self.birim_fiyati_entry.grid(row=3, column=1)

        #işlem butonları
        self.ekle_button = tk.Button(root, text="Ekle", command=self.ekle)
        self.ekle_button.grid(row=4, column=0, columnspan = 1)
        #düzelt
        self.duzelt_button = tk.Button(root, text="Düzelt", command=self.duzelt)
        self.duzelt_button.grid(row=4, column=1, columnspan = 1)
        #Sil
        self.sil_button = tk.Button(root, text="Sil", command=self.sil)
        self.sil_button.grid(row=4, column=2, columnspan = 1)

        #temizle 
        self.temizle_button = tk.Button(root, text="Temizle", command=self.temizle)
        self.temizle_button.grid(row=4, column=3, columnspan = 1)

        #arama çubuğu
        self.arama_cubugu = tk.Entry(root, text="Ara")
        self.arama_cubugu.grid(row=5, column=0)
        self.arama_entry = tk.Entry(root)
        self.arama_entry.grid(row=5, column=1)

        #arama tetikleyicisi
        self.arama_entry.bind("<Return>", self.arama)

        #tablo oluştur
        self.tablo = ttk.Treeview(root, columns=("ID", "Ürün Adı", "Adet", "Birim Fiyatı", "Toplam Değer"), show="headings") 
        self.tablo.heading("ID", text="ID")
        self.tablo.heading("Ürün Adi", text="Ürün Adı")
        self.tablo.heading("Adet", text="Adet")
        self.tablo.heading("Birim Fiyatı", text="Birim Fiyatı")
        self.tablo.heading("Toplam Değer", text="Toplam DeĞer")
        self.tablo.grid (row=6, column=0, columnspan=4)

        #tabloya tıklanınca veri işlemlerini başlat!
        self.tablo.bind("<ButtonRelease-1>", self.satir_sec)

        self.verileri_yukle() #ana metod bitişi!

    def ekle(self):
       

        



if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryTrackingApplication(root)
    root.mainloop()  
       
