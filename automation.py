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

FICHIER_HASH = "last_hash.txt"


# ==============================
# ENVOYER UNE NOTIFICATION
# ==============================

def envoyer_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(
        url,
        data=data,
        timeout=20
    )


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
# PROGRAMME
# ==============================

print("🔎 Vérification du site ISIMS...")

try:

    # Récupérer le contenu du site

    contenu = recuperer_site()

    # Calculer une empreinte du site

    nouvelle_version = hashlib.md5(
        contenu.encode("utf-8")
    ).hexdigest()

    # Vérifier si on possède déjà une ancienne version

    if os.path.exists(FICHIER_HASH):

        with open(
            FICHIER_HASH,
            "r",
            encoding="utf-8"
        ) as fichier:

            ancienne_version = fichier.read().strip()

    else:

        ancienne_version = ""


    # ==============================
    # PREMIERE VERIFICATION
    # ==============================

    if ancienne_version == "":

        with open(
            FICHIER_HASH,
            "w",
            encoding="utf-8"
        ) as fichier:

            fichier.write(nouvelle_version)

        print("✅ Première vérification terminée.")


    # ==============================
    # LE SITE A CHANGE
    # ==============================

    elif nouvelle_version != ancienne_version:

        print("🚨 Nouvelle modification détectée !")

        envoyer_telegram(
            "🔔 NOUVEAUTÉ ISIMS !\n\n"
            "Le site de l'ISIMS vient d'être modifié.\n\n"
            f"🌐 {URL}"
        )

        # Sauvegarder la nouvelle version

        with open(
            FICHIER_HASH,
            "w",
            encoding="utf-8"
        ) as fichier:

            fichier.write(nouvelle_version)

        print("📱 Notification Telegram envoyée.")


    # ==============================
    # AUCUN CHANGEMENT
    # ==============================

    else:

        print("✓ Rien de nouveau.")


except Exception as erreur:

    print("❌ Erreur :", erreur)
