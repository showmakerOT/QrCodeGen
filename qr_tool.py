import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import qrcode
import validators
import time

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Códigos QR Avanzado")
        self.root.geometry("800x900")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f8ff")  # Fondo azul claro

        self.history = []  # Historial de QR generados
        self.current_qr_img = None
        self.current_url = ""

        # Mensaje de bienvenida con colores
        self.welcome_label = tk.Label(root, text="¡Bienvenido a la Herramienta de Generación de QR!", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#2e8b57")
        self.welcome_label.pack(pady=20)

        # Etiqueta para URL con colores
        self.url_label = tk.Label(root, text="Ingresa la URL:", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#4682b4")
        self.url_label.pack(pady=10)

        # Campo de entrada para URL con estilo
        self.url_entry = tk.Entry(root, width=60, font=("Arial", 12), bd=3, relief="sunken", bg="#ffffff", fg="#000000")
        self.url_entry.pack(pady=10)

        # Frame para botones
        button_frame = tk.Frame(root, bg="#f0f8ff")
        button_frame.pack(pady=20)

        # Botón para generar QR con colores avanzados
        self.generate_button = tk.Button(button_frame, text="Generar QR", command=self.generate_qr, font=("Arial", 12, "bold"), bg="#32cd32", fg="white", activebackground="#228b22", activeforeground="white", bd=3, relief="raised")
        self.generate_button.pack(side=tk.LEFT, padx=10)

        # Botón para descargar QR
        self.download_button = tk.Button(button_frame, text="Descargar QR", command=self.download_qr, font=("Arial", 12, "bold"), bg="#ff6347", fg="white", activebackground="#dc143c", activeforeground="white", bd=3, relief="raised", state=tk.DISABLED)
        self.download_button.pack(side=tk.LEFT, padx=10)

        # Etiqueta para tiempo de generación
        self.time_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f8ff", fg="#696969")
        self.time_label.pack(pady=5)

        # Área para mostrar el QR con borde
        self.qr_label = tk.Label(root, bg="#f0f8ff", bd=2, relief="groove")
        self.qr_label.pack(pady=20)

        # Historial
        history_frame = tk.Frame(root, bg="#f0f8ff")
        history_frame.pack(pady=10)

        self.history_label = tk.Label(history_frame, text="Historial de QR:", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#4682b4")
        self.history_label.pack()

        self.history_listbox = tk.Listbox(history_frame, width=70, height=5, font=("Arial", 10), bg="#ffffff", fg="#000000")
        self.history_listbox.pack(pady=5)
        self.history_listbox.bind('<<ListboxSelect>>', self.load_from_history)

        # Etiqueta adicional para instrucciones
        self.instruction_label = tk.Label(root, text="El QR se generará y mostrará aquí.", font=("Arial", 10), bg="#f0f8ff", fg="#696969")
        self.instruction_label.pack(pady=10)

    def generate_qr(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor, ingresa una URL.")
            return
        if not validators.url(url):
            messagebox.showerror("Error", "La URL no es válida.")
            return
        start_time = time.time()
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            self.current_qr_img = img
            self.qr_img = ImageTk.PhotoImage(img)
            self.qr_label.config(image=self.qr_img)
            self.current_url = url
            self.download_button.config(state=tk.NORMAL)
            end_time = time.time()
            generation_time = end_time - start_time
            self.time_label.config(text=f"Tiempo de generación: {generation_time:.4f} segundos")
            # Agregar al historial
            if url not in self.history:
                self.history.append(url)
                self.history_listbox.insert(tk.END, url)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el QR: {str(e)}")

    def download_qr(self):
        if self.current_qr_img is None:
            messagebox.showerror("Error", "No hay QR para descargar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.current_qr_img.save(file_path)
            messagebox.showinfo("Éxito", f"QR guardado en {file_path}")



    def load_from_history(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            url = self.history[index]
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
            self.generate_qr()

if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
