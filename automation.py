import requests
import hashlib
import os
import time
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)
# ==============================
# TES INFORMATIONS
# ==============================

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://isimsf.rnu.tn/"


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

    reponse = requests.get(URL, verify=False)

    return reponse.text


# ==============================
# PROGRAMME
# ==============================

ancienne_version = ""

while True:

    print("🔎 Vérification du site ISIMS...")

    try:

        contenu = recuperer_site()

        nouvelle_version = hashlib.md5(
            contenu.encode()
        ).hexdigest()

        # Première vérification
        if ancienne_version == "":
            ancienne_version = nouvelle_version
            print("✅ Surveillance commencée.")

        # Le site a changé
        elif nouvelle_version != ancienne_version:

            print("🚨 Nouvelle modification détectée !")

            envoyer_telegram(
                "🔔 NOUVEAUTÉ ISIMS !\n\n"
                "Le site de l'ISIMS vient d'être modifié.\n\n"
                f"🌐 {URL}"
            )

            ancienne_version = nouvelle_version

        else:

            print("✓ Rien de nouveau.")

    except Exception as erreur:

        print("❌ Erreur :", erreur)

    # Vérifier toutes les 30 minutes
    time.sleep(300)
