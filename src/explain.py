import requests

LM_URL = "http://localhost:1235/v1/chat/completions"
MODEL = "qwen/qwen3.5-9b"

# Correspondance approximative catégorie UNSW-NB15 -> MITRE ATT&CK
# À vérifier sur https://attack.mitre.org
MITRE = {
    "Reconnaissance": ("Reconnaissance (TA0043)", "T1595 Active Scanning"),
    "Analysis": ("Reconnaissance (TA0043)", "T1595 Active Scanning"),
    "Fuzzers": ("Initial Access (TA0001)", "T1190 Exploit Public-Facing Application"),
    "Exploits": ("Initial Access (TA0001)", "T1190 Exploit Public-Facing Application"),
    "DoS": ("Impact (TA0040)", "T1498 Network Denial of Service"),
    "Backdoor": ("Command and Control (TA0011)", "T1071 Application Layer Protocol"),
    "Shellcode": ("Execution (TA0002)", "T1203 Exploitation for Client Execution"),
    "Worms": ("Lateral Movement (TA0008)", "T1210 Exploitation of Remote Services"),
    "Generic": ("Credential Access (TA0006)", "T1110 Brute Force"),
}

# Signification des états de connexion d'UNSW-NB15
STATES = {
    "INT": "connexion interrompue (pas de fin normale)",
    "FIN": "connexion terminée normalement",
    "CON": "connexion établie",
    "REQ": "requête envoyée",
    "RST": "connexion réinitialisée",
    "ECO": "écho ICMP",
    "CLO": "connexion fermée",
}


def mitre_for(categorie):
    return MITRE.get(categorie, ("Non déterminée", "-"))


def explain_alert(row):
    tactique, technique = mitre_for(row["attack_cat"])
    etat = STATES.get(str(row["state"]), "état non documenté")

    prompt = f"""Explique en français, en 4 phrases courtes maximum, cette alerte de sécurité.

Données du flux :
- protocole : {row['proto']}, service : {row['service']}
- état de connexion : {row['state']} ({etat})
- durée : {row['dur']:.3f} s
- octets envoyés : {row['sbytes']}, octets reçus : {row['dbytes']}
- score de détection (modèle binaire normal/attaque) : {row['proba']:.2f}
- étiquette du jeu de données : {row['attack_cat']}
- correspondance MITRE ATT&CK indicative : {tactique} / {technique}

Règles :
1. Le modèle de détection prédit seulement « attaque » ou « normal ».
   La catégorie « {row['attack_cat']} » est l'étiquette du jeu de données :
   n'écris JAMAIS que le modèle l'a identifiée ou détectée.
2. Ne tire aucune conclusion que les données ne prouvent pas
   (un seul flux ne prouve pas un déni de service). Si les données ne permettent
   pas de conclure, dis-le.
3. Structure : ce qui est observé, le risque possible, une action recommandée.
/no_think"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system",
             "content": "Tu es analyste SOC. Réponds directement en français, sans réflexion préalable, de façon prudente et factuelle."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 4000,
        "chat_template_kwargs": {"enable_thinking": False},
    }

    r = requests.post(LM_URL, json=payload, timeout=900)
    if not r.ok:
        payload.pop("chat_template_kwargs")
        r = requests.post(LM_URL, json=payload, timeout=900)
    if not r.ok:
        raise RuntimeError(f"{r.status_code} : {r.text[:300]}")

    choix = r.json()["choices"][0]
    message = choix["message"]
    texte = (message.get("content") or "").strip()
    if "</think>" in texte:
        texte = texte.split("</think>")[-1].strip()

    if not texte:
        raise RuntimeError(
            f"Réponse vide (finish_reason={choix.get('finish_reason')}). "
            "Désactive la réflexion dans LM Studio ou utilise un modèle plus léger."
        )
    return texte