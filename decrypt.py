import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from cryptography.fernet import Fernet
import base64

# === Core Logic ===

def load_key(key_path):
    with open(key_path, "rb") as f:
        return f.read()

def extract_message_from_image(image_path):
    img = Image.open(image_path)
    binary_data = ''
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            pixel = pixels[x, y]
            for n in range(3):
                binary_data += str(pixel[n] & 1)

    eof_index = binary_data.find('1111111111111110')
    if eof_index == -1:
        raise ValueError("EOF marker not found. No hidden data.")

    binary_data = binary_data[:eof_index]

    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    return ''.join(chars)

def decrypt_message(encrypted_message, key):
    encrypted = base64.urlsafe_b64decode(encrypted_message.encode())
    fernet = Fernet(key)
    return fernet.decrypt(encrypted).decode()

# === GUI App ===

class DecryptStegoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Extract & Decrypt Message from Image")
        self.master.geometry("550x350")

        self.image_path = ""
        self.key_path = ""

        tk.Button(master, text="Browse Image", command=self.browse_image).pack(pady=10)
        tk.Button(master, text="Browse Secret Key", command=self.browse_key).pack(pady=10)
        tk.Button(master, text="Decrypt", command=self.extract_and_decrypt).pack(pady=15)

        self.output_label = tk.Label(master, text="Decrypted Message:")
        self.output_label.pack()

        self.output_text = tk.Text(master, height=10, width=60)
        self.output_text.pack()

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Selected", f"Selected Image:\n{file_path}")

    def browse_key(self):
        file_path = filedialog.askopenfilename(filetypes=[("Key File", "*.key")])
        if file_path:
            self.key_path = file_path
            messagebox.showinfo("Key Selected", f"Selected Key:\n{file_path}")

    def extract_and_decrypt(self):
        if not self.image_path or not self.key_path:
            messagebox.showerror("Missing Input", "Please select both image and key file.")
            return

        try:
            key = load_key(self.key_path)
            encrypted_msg = extract_message_from_image(self.image_path)
            decrypted_msg = decrypt_message(encrypted_msg, key)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, decrypted_msg)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt message:\n{str(e)}")

# === Run App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = DecryptStegoApp(root)
    root.mainloop()
