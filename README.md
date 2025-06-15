# 🕵️‍♂️ StegoCrypt: Hide Text in Images Using Cryptography

> Edunet Foundation

**StegoCrypt** is a Python-based project that allows you to **securely hide encrypted messages inside images** using **AES encryption** and **LSB steganography**. The decryption process requires a **key file** that was generated during encryption, ensuring that only someone with the right key can retrieve the hidden message.

---

## 🔐 Features

* 🔏 **AES Encryption** for message confidentiality
* 🖼️ **Image Steganography (LSB)** for hiding encrypted data in images
* 🔑 **Key File-based Decryption** (no password input)
* 🧪 Simple CLI-based scripts
* 🧰 Easy to integrate into other tools or workflows

---

## 📁 Project Structure

```
StegoCrypt/
├── encrypt.py     # Encrypt message & hide in image
├── decrypt.py     # Extract & decrypt message (needs key file)
├── output.png     # Output image with hidden encrypted data
├── secret.key     # AES key file generated during encryption
└── README.md      # Project documentation
```

---

## 🧪 Requirements

* Python 3.x
* `Pillow` – image handling
* `cryptography` – AES encryption/decryption

Install the required libraries:

```bash
pip install pillow cryptography
```

---

## 🚀 How to Use

### 🔒 Step 1: Encrypt and Hide a Message

```bash
python encrypt.py
```

* Input your **secret message**.
* Choose a **cover image** (PNG recommended).
* Script will:

  * Generate a secure AES key and save it as `secret.key`
  * Encrypt the message using AES
  * Embed the encrypted data in the image using **LSB steganography**
  * Save the output as `output.png`

![Screenshot 2025-06-15 112041](https://github.com/user-attachments/assets/bbc34eb7-27f5-4a2b-a326-a4ddecac71ac)

🔑 **Important:** Save the `secret.key` file securely. You’ll need it for decryption!

---

### 🔓 Step 2: Reveal and Decrypt the Message

```bash
python decrypt.py
```

* Input the **stego image** (`output.png`)
* Provide the **key file** (`secret.key`)
* Script will:

  * Extract hidden data from the image
  * Decrypt the data using the AES key from the key file
  * Display the original secret message

![Screenshot 2025-06-15 115128](https://github.com/user-attachments/assets/635ad541-95a2-4d32-8183-86f349729fd2)

---

## 🔒 Security Notes

* The **AES key is randomly generated** and stored in `secret.key`.
* Only someone with both the **stego image** and the **key file** can decrypt the message.
* Avoid sharing the key file with unauthorized users.
* This tool is for educational/demo use, not recommended for secure messaging in production.

---

## 📸 Visual Example

| Input Image                                                                               | Output Image |
|-------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| ![input](https://github.com/user-attachments/assets/590c81b5-36c1-414f-8f30-4e8bcb8f5dab) | ![output](https://github.com/user-attachments/assets/fe245b87-8c97-4af1-8635-b32108648900) |

> ✅ Encrypted Image (`output.png`) looks visually identical to the original.

> ❌ Hidden content is not visible without the key.

---

## 📌 Future Enhancements

* ✅ Drag and drop interface
* ✅ Optional password-based encryption
* ✅ Support for audio/video steganography
