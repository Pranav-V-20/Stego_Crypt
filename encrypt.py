import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from cryptography.fernet import Fernet
import base64
import os

# === Encryption Functions ===

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists("secret.key"):
        generate_key()
    with open("secret.key", "rb") as f:
        return f.read()

def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

# === Steganography Functions ===

def message_to_bits(message):
    return ''.join(format(ord(char), '08b') for char in message)

def hide_message_in_image(image_path, output_path, message):
    img = Image.open(image_path)
    binary_message = message_to_bits(message) + '1111111111111110'  # EOF marker
    data_index = 0
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            for n in range(3):  # R, G, B
                if data_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            pixels[x, y] = tuple(pixel)
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    img.save(output_path)

# === GUI Code ===

class StegoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Steganography with Encryption")
        self.master.geometry("500x300")
        self.image_path = ""

        self.label = tk.Label(master, text="Enter message to hide:")
        self.label.pack(pady=10)

        self.text_entry = tk.Text(master, height=5, width=50)
        self.text_entry.pack()

        self.browse_button = tk.Button(master, text="Browse Image", command=self.browse_image)
        self.browse_button.pack(pady=10)

        self.encrypt_button = tk.Button(master, text="Encrypt & Hide Message", command=self.encrypt_and_hide)
        self.encrypt_button.pack(pady=10)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Selected", f"Image selected:\n{file_path}")

    def encrypt_and_hide(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image.")
            return

        message = self.text_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide.")
            return

        key = load_key()
        encrypted = encrypt_message(message, key)

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not save_path:
            return

        try:
            hide_message_in_image(self.image_path, save_path, encrypted)
            messagebox.showinfo("Success", f"Message successfully hidden in:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to hide message:\n{str(e)}")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
