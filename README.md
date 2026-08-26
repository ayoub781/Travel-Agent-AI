# Travel Agent AI — Agent IA météo & vols

Un agent IA qui scrape les données météo et les prix de vols en temps réel pour recommander la meilleure période de voyage.

---

## Demo

```
User : "Quelle est la meilleure période pour aller à Tokyo ?"

Agent :
  Tour 1 → scrape_meteo("Tokyo")        → températures min/max par mois
  Tour 2 → scrape_vols("Paris","Tokyo") → prix estimés par mois
  Tour 3 → analyse et répond :
           "Octobre-novembre est idéal :
            - Météo : 17-22°C, agréable
            - Prix : ~450€ (moins cher qu'en été)
            - Éviter juillet-août : 30-32°C + 850€"
```

---

## Architecture

```
Selenium scrape timeanddate.com  →  meteo.json
Selenium scrape rome2rio.com     →  vols.json
                ↓
        Function Calling (tools OpenAI)
        get_meteo(destination)
        get_vols(origine, destination)
                ↓
        Agent ReAct (boucle agentique)
        GPT raisonne → appelle les tools → raisonne → répond
                ↓
        API Flask  →  POST /chat
                ↓
        Interface Streamlit
```

---

## Pourquoi cet outil vs ChatGPT ?

ChatGPT répond depuis ses données d'entraînement figées. Notre agent scrape les vraies données au moment où tu poses la question.

```
ChatGPT : "Les vols Paris-Tokyo coûtent généralement entre 600€ et 1200€"
           ↑ estimation générale, données passées

Notre agent : "Aujourd'hui le vol du 15 octobre est à 487€
               Météo à Tokyo en octobre : 22°C ensoleillé — idéal !"
               ↑ données scrappées à l'instant
```

| | ChatGPT classique | ChatGPT browsing | Notre agent |
|---|---|---|---|
| Données temps réel | ❌ | ✅ | ✅ |
| Contrôle total | ❌ | ❌ | ✅ |
| Personnalisable | ❌ | ❌ | ✅ |
| Gratuit | ❌ (Pro) | ❌ (Pro) | ✅ |
| Open source | ❌ | ❌ | ✅ |

---

## Stack technique

| Outil | Rôle |
|-------|------|
| Python | Langage principal |
| Selenium | Scraping web dynamique |
| OpenAI GPT-4o-mini | LLM + Function Calling |
| Flask | API REST |
| Streamlit | Interface utilisateur |
| JSON | Stockage des données scrappées |

---

## Sources de données

| Donnée | Source | Méthode |
|--------|--------|---------|
| Météo par destination | timeanddate.com | Selenium |
| Prix de vols | rome2rio.com | Selenium |

---

## Structure du projet

```
travel-agent/
├── scraping/
│   ├── meteo.py          # scraper timeanddate.com
│   ├── vols.py           # scraper rome2rio.com
│   ├── meteo.json        # données météo scrappées
│   └── vols.json         # données vols scrappées
├── chatbot/
│   ├── chatbot.py        # classe Chatbot + boucle agentique
│   └── tools.py          # fonctions get_meteo, get_vols
├── app.py                # API Flask
├── streamlit_app.py      # interface Streamlit
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/ton-user/travel-agent
cd travel-agent
pip install -r requirements.txt
```

Crée un fichier `.env` :
```
OPENAI_API_KEY=sk-...
```

---

## Lancement

```bash
# 1. Scraper les données
python scraping/meteo.py
python scraping/vols.py

# 2. Lancer l'API Flask
python app.py

# 3. Lancer l'interface
streamlit run streamlit_app.py
```

---

## Concepts techniques implémentés
- **Scraping dynamique** - Il faut arriver à faire en sorte que la destination.. demandé par le prompt utilisateur soit directement recherché dans notre scraping. Il ne faut donc pas ecrire en dur lors de notre scraping (ie. send_keys("Japon") pour rechercher le japon)
- **Function Calling** — GPT appelle les fonctions Python selon la question
- **Boucle agentique** — GPT décide seul combien de tours faire (ReAct pattern)
- **Fenêtre de contexte** — Nous utiliserons pour cela un rag, car le probleme du tronquage est qu'il peut couper l'historique au mauvais endorit.
- **API REST** — POST /chat exposé via Flask
- **Scraping anti-détection** — User-Agent, délais aléatoires, disable-blink-features

---

## Roadmap

- [x] Scraper météo Tokyo (timeanddate.com)
- [ ] Scraper prix vols (rome2rio.com)
- [ ] Intégrer dans l'agent via function calling
- [ ] Boucle agentique ReAct
- [ ] API Flask
- [ ] Interface Streamlit
- [ ] Métriques d'évaluation (précision, recall, RAGAS)
- [ ] Multi-destinations (Japon, Vietnam, Thaïlande...)
- [ ] Alertes prix par email


