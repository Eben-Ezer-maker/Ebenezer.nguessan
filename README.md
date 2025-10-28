👋 Hi, I'm Eben-Ezer N’guessan

🎓 Magistère student in Development Economics at CERDI – Université Clermont Auvergne
💡 Passionate about data-driven public policy, development finance, and trade economics
📍 Based in Clermont-Ferrand, France
📧 ebenezeressan@gmail.com

🔗 LinkedIn

---

## 📈 Projet Streamlit — ITC Tariff Stress Lab

Ce dépôt contient une application web Streamlit développée pour accompagner les décideurs de l’International Trade Centre (Genève) face aux surtaxes américaines de l’ère Trump. L’outil permet :

- d’explorer une base indicative de secteurs touchés et les mesures de sauvegarde en place,
- de simuler l’impact financier d’un choc tarifaire selon la valeur exportée et le pass-through supposé,
- de comparer un scénario d’atténuation (dérogations, diversification) aux surtaxes historiques,
- de prioriser des marchés alternatifs grâce à un tableau de synthèse et des recommandations automatiques,
- de constituer un portefeuille d’analyses exportable au format CSV.

### 🚀 Comment lancer l’application

```bash
python -m venv .venv
source .venv/bin/activate  # sous Windows : .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Une fois le serveur Streamlit démarré, ouvrir le lien local affiché (généralement http://localhost:8501) pour interagir avec le tableau de bord.

### 🧩 Structure du projet

- `app.py` — logique Streamlit, calculs d’impact et génération des recommandations.
- `data/tariff_scenarios.csv` — taux de droits avant/après et mesures de sauvegarde.
- `data/alternative_markets.csv` — marchés de diversification avec tarifs moyens.
- `requirements.txt` — dépendances Python pour exécuter l’application.

### 🔄 Personnalisation

- Remplacez les fichiers CSV par vos données maison pour couvrir d’autres secteurs ou marchés.
- Connectez-vous à une API tarifaire (ITC Market Access Map, WTO Tariff Download Facility…) pour des mises à jour dynamiques.
- Ajoutez un module d’élasticité-prix pour estimer l’effet sur les volumes exportés.

---

## 🧠 À propos

I’m a data-driven economist passionate about leveraging quantitative analysis, econometrics, and data science to inform policy decisions in developing economies. My work focuses on topics such as trade diversification, poverty analysis, and macroeconomic modeling.

Currently pursuing:

- 🎓 Magistère in Development Economics (CERDI)
- 🎓 DU Sorbonne Data Analytics (Panthéon-Sorbonne University)

I aspire to join international organizations like the World Bank, IMF, or WTO to contribute to evidence-based economic policymaking.

## 🚀 Featured Projects

### 📊 Export Diversification & Economic Growth

Objective: Evaluate whether export concentration or diversification influences economic growth.
Tools: R, EViews, WITS, World Bank API

- Built an international panel dataset (LMICs vs. developed countries)
- Applied econometric models (fixed/random effects, robustness checks)
- Found heterogeneous impacts depending on country group

### 💰 Monetary Analysis of Poverty – Senegal & Guinea-Bissau

Objective: Measure and compare poverty using household data from EHCVM 2018–2022.
Tools: R (ggplot2, dplyr), Python (Pandas), QGIS

- Computed FGT, Watts, and Chakravarty indices
- Visualized poverty depth and inequality
- Produced policy recommendations for UEMOA governments

### 🏛️ Macroeconomic Modeling – France 2023

Objective: Build a Social Accounting Matrix and simulate macroeconomic policy shocks.
Tools: Excel, R, EViews

- Designed the SAM of France
- Modeled fiscal and demand-side policies
- Simulated scenarios and assessed multiplier effects

### 👨‍👩‍👧 Family Economics – Transfers & Education Gaps

Objective: Analyze the impact of household transfers on education by gender.
Tools: R, STATA

- Created a household-level dataset
- Compared patterns between Senegal and Guinea-Bissau
- Identified gender gaps in educational outcomes

## 🧩 Skills

**Technical**: Python | R | SQL | EViews | Power BI | Excel | LaTeX | Machine Learning | Cloud Computing

**Soft Skills**: Analytical Thinking • Adaptability • Collaboration • Time Management • Empathy

## 🌍 Goals

I aim to combine quantitative economics and data science to support inclusive growth policies and fiscal optimization in developing countries — particularly in Sub-Saharan Africa.

## ⚡ Fun Fact

When I’m not analyzing data, I explore the intersection between AI and development policy, and I’m always curious about how technology can empower better governance.
