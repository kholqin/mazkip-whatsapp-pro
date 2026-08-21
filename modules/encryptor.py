#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — Encryptor Module
Enkripsi AES-256 untuk target list, konfigurasi, dan session
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, json, base64, hashlib
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAIL = True
except ImportError:
    CRYPTO_AVAIL = False

KEY_FILE = Path.home() / "mazkip-whatsapp-pro" / ".mw_key"

class Encryptor:
    """Enkripsi dan dekripsi data tools"""

    def __init__(self):
        self.key = None
        self._init_key()

    def _init_key(self):
        if not CRYPTO_AVAIL:
            print(f"{Y}[!] cryptography tidak terinstall. Enkripsi dinonaktifkan.")
            return

        if KEY_FILE.exists():
            with open(KEY_FILE, 'rb') as f:
                self.key = f.read()
        else:
            # Generate key baru
            password = hashlib.sha256(b"M4zk1Play_Nusantara_2026_ANONIMUS").digest()
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
            key = base64.urlsafe_b64encode(kdf.derive(password))

            # Simpan key
            KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(KEY_FILE, 'wb') as f:
                f.write(key)
            self.key = key
            os.chmod(KEY_FILE, 0o600)  # Hanya owner yang bisa baca

    def encrypt(self, data):
        """Enkripsi data string"""
        if not CRYPTO_AVAIL or not self.key:
            return data
        try:
            f = Fernet(self.key)
            return f.encrypt(data.encode()).decode()
        except Exception as e:
            print(f"{R}[!] Enkripsi gagal: {e}")
            return data

    def decrypt(self, token):
        """Dekripsi data terenkripsi"""
        if not CRYPTO_AVAIL or not self.key:
            return token
        try:
            f = Fernet(self.key)
            return f.decrypt(token.encode()).decode()
        except:
            return token  # Mungkin belum terenkripsi

    def encrypt_file(self, filepath):
        """Enkripsi file"""
        if not filepath.exists():
            return False
        with open(filepath, 'r') as f:
            data = f.read()
        encrypted = self.encrypt(data)
        with open(filepath, 'w') as f:
            f.write(encrypted)
        # Rename jadi .enc
        filepath.rename(filepath.with_suffix('.enc'))
        return True

    def decrypt_file(self, filepath):
        """Dekripsi file"""
        enc_path = filepath.with_suffix('.enc') if filepath.suffix != '.enc' else filepath
        if not enc_path.exists():
            return False
        with open(enc_path, 'r') as f:
            data = f.read()
        decrypted = self.decrypt(data)
        out_path = enc_path.with_suffix('') if enc_path.suffix == '.enc' else enc_path
        with open(out_path, 'w') as f:
            f.write(decrypted)
        return True

    def wipe_file(self, filepath, passes=3):
        """Wipe file aman (secure delete)"""
        if not filepath.exists():
            return
        length = filepath.stat().st_size
        for _ in range(passes):
            # Write random data
            with open(filepath, 'wb') as f:
                f.write(os.urandom(length))
        filepath.unlink()
        print(f"{G}[✓] File {filepath.name} telah di-wipe secara aman!")

enc = Encryptor()
