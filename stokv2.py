import tkinter as tk
from tkinter import ttk
import sqlite3

class InventoryTrackingApplication:
    def __init__(self, root):
        # Ana pencereyi oluştur
        self.root = root
        self.root.title("Inventory Tracking Application")
        self.setup_database()
        self.create_input_fields()
        self.create_table()
        self.load_data()

    def setup_database(self):
        # Veritabanı bağlantısını ve tabloyu oluştur
        self.conn = sqlite3.connect('stock_tracking.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks(
                id TEXT PRIMARY KEY,
                urun_adi TEXT,
                adet INTEGER,
                birim_fiyati REAL,
                toplam_deger REAL
            )
        """)
        self.conn.commit()

    def create_input_fields(self):
        # Giriş alanları ve butonlar
        self.create_label_and_entry("ID:", 0, 0, "id_entry")
        self.create_label_and_entry("Ürün Adı:", 1, 0, "urun_adi_entry")
        self.create_label_and_entry("Adet:", 2, 0, "adet_entry")
        self.create_label_and_entry("Birim Fiyatı:", 3, 0, "birim_fiyati_entry")

        self.ekle_button = tk.Button(self.root, text="Ekle", command=self.add_record)
        self.ekle_button.grid(row=4, column=0, padx=5, pady=5)

        self.duzelt_button = tk.Button(self.root, text="Düzelt", command=self.update_record)
        self.duzelt_button.grid(row=4, column=1, padx=5, pady=5)

        self.sil_button = tk.Button(self.root, text="Sil", command=self.delete_record)
        self.sil_button.grid(row=4, column=2, padx=5, pady=5)

        self.temizle_button = tk.Button(self.root, text="Temizle", command=self.clear_entries)
        self.temizle_button.grid(row=4, column=3, padx=5, pady=5)

        self.arama_entry = tk.Entry(self.root)
        self.arama_entry.grid(row=5, column=1, padx=5, pady=5)
        self.arama_entry.bind("<KeyRelease>", self.search)

    def create_label_and_entry(self, text, row, col, entry_attr):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=col, padx=5, pady=5)
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=col + 1, padx=5, pady=5)
        setattr(self, entry_attr, entry)

    def create_table(self):
        # TreeView tablosu oluştur
        self.tablo = ttk.Treeview(self.root, columns=("ID", "Ürün Adı", "Adet", "Birim Fiyatı", "Toplam Değer"), show="headings")
        for col in self.tablo["columns"]:
            self.tablo.heading(col, text=col)
        self.tablo.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
        self.tablo.bind("<ButtonRelease-1>", self.select_row)

    def add_record(self):
        # Yeni kayıt ekle
        try:
            id, urun_adi, adet, birim_fiyati = self.get_entries()
            toplam_deger = self.calculate_total_value(adet, birim_fiyati)
            self.cursor.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?)", (id, urun_adi, adet, birim_fiyati, toplam_deger))
            self.conn.commit()
            self.tablo.insert("", "end", values=(id, urun_adi, adet, birim_fiyati, toplam_deger))
            self.clear_entries()
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")

    def update_record(self):
        # Kayıt güncelle
        selected_item = self.tablo.selection()
        if selected_item:
            try:
                id, urun_adi, adet, birim_fiyati = self.get_entries()
                toplam_deger = self.calculate_total_value(adet, birim_fiyati)
                self.cursor.execute("UPDATE stocks SET urun_adi=?, adet=?, birim_fiyati=?, toplam_deger=? WHERE id=?", 
                                    (urun_adi, adet, birim_fiyati, toplam_deger, id))
                self.conn.commit()
                self.tablo.item(selected_item, values=(id, urun_adi, adet, birim_fiyati, toplam_deger))
                self.clear_entries()
            except sqlite3.Error as e:
                print(f"Güncelleme hatası: {e}")

    def delete_record(self):
        # Kayıt sil
        selected_item = self.tablo.selection()
        if selected_item:
            try:
                id = self.tablo.item(selected_item)['values'][0]
                self.cursor.execute("DELETE FROM stocks WHERE id=?", (id,))
                self.conn.commit()
                self.tablo.delete(selected_item)
                self.clear_entries()
            except sqlite3.Error as e:
                print(f"Silme hatası: {e}")

    def search(self, event):
        # Arama işlevi
        search_text = self.arama_entry.get().lower()
        for item in self.tablo.get_children():
            values = self.tablo.item(item, "values")
            if search_text in values[0].lower() or search_text in values[1].lower():
                self.tablo.selection_set(item)
                self.tablo.see(item)
            else:
                self.tablo.selection_remove(item)

    def select_row(self, event):
        # Satır seçimi
        selected_item = self.tablo.selection()
        if selected_item:
            values = self.tablo.item(selected_item)["values"]
            self.fill_entries(values)

    def get_entries(self):
        # Giriş alanlarından veri al
        return (self.id_entry.get(), self.urun_adi_entry.get(), int(self.adet_entry.get()), float(self.birim_fiyati_entry.get()))

    def fill_entries(self, values):
        # Giriş alanlarını doldur
        self.clear_entries()
        self.id_entry.insert(0, values[0])
        self.urun_adi_entry.insert(0, values[1])
        self.adet_entry.insert(0, values[2])
        self.birim_fiyati_entry.insert(0, values[3])

    def clear_entries(self):
        # Giriş alanlarını temizle
        self.id_entry.delete(0, tk.END)
        self.urun_adi_entry.delete(0, tk.END)
        self.adet_entry.delete(0, tk.END)
        self.birim_fiyati_entry.delete(0, tk.END)

    def calculate_total_value(self, adet, birim_fiyati):
        return adet * birim_fiyati

    def load_data(self):
        # Verileri tabloya yükle
        try:
            for row in self.cursor.execute("SELECT * FROM stocks"):
                self.tablo.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"Veri yükleme hatası: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryTrackingApplication(root)
    root.mainloop()
