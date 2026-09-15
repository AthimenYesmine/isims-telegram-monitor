import requests
import hashlib
import os
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

# ==============================
# INFORMATIONS
# ==============================

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://isimsf.rnu.tn/"
HASH_FILE = "last_hash.txt"


# ==============================
# ENVOYER UNE NOTIFICATION
# ==============================

def envoyer_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


# ==============================
# RECUPERER LE SITE
# ==============================

def recuperer_site():
    reponse = requests.get(
        URL,
        verify=False,
        timeout=30
    )

    reponse.raise_for_status()

    return reponse.text


# ==============================
# LIRE L'ANCIEN HASH
# ==============================

def lire_ancien_hash():

    if os.path.exists(HASH_FILE):

        with open(HASH_FILE, "r") as fichier:
            return fichier.read().strip()

    return ""


# ==============================
# SAUVEGARDER LE NOUVEAU HASH
# ==============================

def sauvegarder_hash(nouveau_hash):

    with open(HASH_FILE, "w") as fichier:
        fichier.write(nouveau_hash)


# ==============================
# PROGRAMME PRINCIPAL
# ==============================

print("🔎 Vérification du site ISIMS...")

try:

    contenu = recuperer_site()

    nouvelle_version = hashlib.md5(
        contenu.encode()
    ).hexdigest()

    ancienne_version = lire_ancien_hash()

    # Première vérification
    if ancienne_version == "":

        sauvegarder_hash(nouvelle_version)

        print("✅ Première vérification effectuée.")

    # Le site a changé
    elif nouvelle_version != ancienne_version:

        print("🚨 Nouvelle modification détectée !")

        envoyer_telegram(
            "🔔 NOUVEAUTÉ ISIMS !\n\n"
            "Le site de l'ISIMS vient d'être modifié.\n\n"
            f"🌐 {URL}"
        )

        sauvegarder_hash(nouvelle_version)

        print("✅ Nouveau hash sauvegardé.")

    # Rien n'a changé
    else:

        print("✓ Rien de nouveau.")

        sauvegarder_hash(nouvelle_version)

except Exception as erreur:

    print("❌ Erreur :", erreur)
    raise
