"""Streamlit app for analyzing tariff changes and advising trade strategy."""
from __future__ import annotations

from pathlib import Path
from typing import List

import altair as alt
import pandas as pd
import streamlit as st

APP_TITLE = "ITC - Analyse des surtaxes américaines"
DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_tariff_data() -> pd.DataFrame:
    """Load baseline and Trump-era tariff data."""
    return pd.read_csv(DATA_DIR / "tariff_scenarios.csv")


@st.cache_data
def load_market_data() -> pd.DataFrame:
    """Load potential alternative market information."""
    return pd.read_csv(DATA_DIR / "alternative_markets.csv")


def _init_session_state() -> None:
    """Ensure Streamlit session state contains required keys."""
    if "saved_scenarios" not in st.session_state:
        st.session_state["saved_scenarios"] = []


def display_header() -> None:
    st.title(APP_TITLE)
    st.caption(
        "Outil d'aide à la décision pour quantifier l'impact des variations de droits de douane "
        "et proposer des pistes de stratégie commerciale."
    )


def sidebar_inputs(tariff_df: pd.DataFrame) -> dict:
    st.sidebar.header("Paramètres de l'analyse")

    sector = st.sidebar.selectbox(
        "Secteur exporté vers les États-Unis",
        options=sorted(tariff_df["sector"].unique()),
    )

    selected_row = tariff_df.loc[tariff_df["sector"] == sector].iloc[0]

    annual_value = st.sidebar.number_input(
        "Valeur annuelle exportée (en millions USD)",
        min_value=0.0,
        value=12.0,
        step=0.5,
    )

    passthrough = st.sidebar.slider(
        "Part du tarif répercutée sur les prix (pass-through)",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.05,
    )

    negotiation_rate = st.sidebar.slider(
        "Tarif espéré après mesures d'atténuation",
        min_value=float(selected_row["baseline_tariff"]),
        max_value=max(float(selected_row["trump_tariff"]) * 1.2, 35.0),
        value=float(selected_row["trump_tariff"]) * 0.7,
        help="Estimation d'un tarif moyen après recours, dérogations ou diversification des fournisseurs.",
    )

    target_market = st.sidebar.selectbox(
        "Marché alternatif prioritaire",
        options=["Maintien sur le marché américain"]
        + load_market_data()["market"].sort_values().tolist(),
    )

    return {
        "sector": sector,
        "annual_value": annual_value,
        "passthrough": passthrough,
        "negotiation_rate": negotiation_rate,
        "target_market": target_market,
        "selected_row": selected_row,
    }


def compute_impacts(params: dict) -> dict:
    selected_row = params["selected_row"]
    base_rate = float(selected_row["baseline_tariff"])
    trump_rate = float(selected_row["trump_tariff"])
    negotiation_rate = float(params["negotiation_rate"])
    value = float(params["annual_value"])

    base_cost = value * base_rate / 100
    trump_cost = value * trump_rate / 100
    negotiated_cost = value * negotiation_rate / 100

    additional_cost = trump_cost - base_cost
    mitigated_savings = trump_cost - negotiated_cost

    passthrough = params["passthrough"]
    exporter_absorption = additional_cost * (1 - passthrough)
    client_cost = additional_cost * passthrough

    pressure_index = (trump_rate - base_rate) * (value / 10)

    risk_level = "Élevé"
    if pressure_index < 15:
        risk_level = "Modéré"
    if pressure_index < 6:
        risk_level = "Faible"

    return {
        "base_rate": base_rate,
        "trump_rate": trump_rate,
        "negotiation_rate": negotiation_rate,
        "base_cost": base_cost,
        "trump_cost": trump_cost,
        "negotiated_cost": negotiated_cost,
        "additional_cost": additional_cost,
        "mitigated_savings": mitigated_savings,
        "exporter_absorption": exporter_absorption,
        "client_cost": client_cost,
        "pressure_index": pressure_index,
        "risk_level": risk_level,
    }


def render_overview(tariff_df: pd.DataFrame) -> None:
    st.subheader("Panorama des surtaxes")
    st.dataframe(
        tariff_df,
        use_container_width=True,
        hide_index=True,
    )

    top_impacts = tariff_df.assign(
        tariff_delta=lambda df: df["trump_tariff"] - df["baseline_tariff"]
    ).sort_values("tariff_delta", ascending=False)

    chart = (
        alt.Chart(top_impacts)
        .mark_bar(color="#f97316")
        .encode(
            x=alt.X("tariff_delta", title="Hausse de tarif (points de pourcentage)"),
            y=alt.Y("sector", sort="-x", title="Secteur"),
            tooltip=["sector", "baseline_tariff", "trump_tariff", "safeguard_measure"],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)


def render_results(params: dict, metrics: dict) -> None:
    selected_row = params["selected_row"]

    st.subheader("Résultats de la simulation")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tarif moyen 2017", f"{metrics['base_rate']:.1f}%")
    c2.metric("Tarif sous administration Trump", f"{metrics['trump_rate']:.1f}%")
    c3.metric("Scénario atténué", f"{metrics['negotiation_rate']:.1f}%")

    st.markdown(
        f"**HS {selected_row['hs_code']} – {selected_row['description']}**"
    )
    st.write(selected_row["safeguard_measure"])

    chart_df = pd.DataFrame(
        {
            "Situation": [
                "Avant Trump",
                "Après Trump",
                "Scénario atténué",
            ],
            "Tarif moyen (%)": [
                metrics["base_rate"],
                metrics["trump_rate"],
                metrics["negotiation_rate"],
            ],
        }
    )

    chart = (
        alt.Chart(chart_df)
        .mark_bar()
        .encode(x="Situation", y="Tarif moyen (%)", color=alt.Color("Situation", legend=None))
        .properties(height=280)
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("### Incidence financière estimée")
    col_a, col_b = st.columns(2)
    col_a.metric("Coût annuel pré-2018", f"{metrics['base_cost']:.2f} M USD")
    col_a.metric("Coût sous surtaxe", f"{metrics['trump_cost']:.2f} M USD")
    col_a.metric("Surcoût net", f"{metrics['additional_cost']:.2f} M USD")

    col_b.metric("Économie visée", f"{metrics['mitigated_savings']:.2f} M USD")
    col_b.metric("Impact absorbé par l'exportateur", f"{metrics['exporter_absorption']:.2f} M USD")
    col_b.metric("Impact répercuté au client", f"{metrics['client_cost']:.2f} M USD")

    st.info(
        f"Indice de pression commerciale : **{metrics['pressure_index']:.1f}** | Niveau de risque : **{metrics['risk_level']}**"
    )

    st.markdown("### Recommandations préliminaires")
    recommendations = build_recommendations(params, metrics)
    for item in recommendations:
        st.write(f"- {item}")


def build_recommendations(params: dict, metrics: dict) -> List[str]:
    suggestions: List[str] = []
    risk = metrics["risk_level"]
    additional_cost = metrics["additional_cost"]
    mitigated_savings = metrics["mitigated_savings"]
    negotiation_rate = metrics["negotiation_rate"]
    target_market = params["target_market"]

    if risk == "Élevé":
        suggestions.append(
            "Prioriser une négociation ciblée avec l'USTR et documenter les chaînes de valeur pour obtenir des dérogations."
        )
    elif risk == "Modéré":
        suggestions.append(
            "Maintenir le suivi juridique et renforcer la communication avec les importateurs américains."
        )
    else:
        suggestions.append("Surveiller l'évolution des mesures sans mobiliser de ressources supplémentaires majeures.")

    if mitigated_savings > additional_cost * 0.4:
        suggestions.append(
            "Accélérer les démarches d'atténuation : preuves d'origine, recours aux exclusions temporaires et optimisation douanière."
        )

    market_df = load_market_data()
    if target_market != "Maintien sur le marché américain":
        market_row = market_df.loc[market_df["market"] == target_market].iloc[0]
        suggestions.append(
            f"Diversifier vers {target_market} (tarif moyen {market_row['avg_tariff']}%) – {market_row['notes']}."
        )
    else:
        suggestions.append(
            "Étudier un scénario de re-localisation partielle pour réduire la dépendance aux composants sensibles."
        )

    if negotiation_rate <= metrics["base_rate"] * 1.2:
        suggestions.append(
            "Construire un dossier économique montrant l'effet sur l'emploi américain pour soutenir la demande d'exemption."
        )

    return suggestions


def render_saved_scenarios(params: dict, metrics: dict) -> None:
    st.markdown("### Capitalisation des analyses")
    if st.button("Enregistrer cette analyse"):
        st.session_state["saved_scenarios"].append(
            {
                "Secteur": params["sector"],
                "Valeur exportée (M USD)": params["annual_value"],
                "Tarif Trump (%)": metrics["trump_rate"],
                "Tarif atténué (%)": metrics["negotiation_rate"],
                "Surcoût net (M USD)": metrics["additional_cost"],
                "Économie visée (M USD)": metrics["mitigated_savings"],
                "Marché prioritaire": params["target_market"],
                "Risque": metrics["risk_level"],
            }
        )
        st.success("Analyse enregistrée dans la session en cours.")

    if st.session_state["saved_scenarios"]:
        history_df = pd.DataFrame(st.session_state["saved_scenarios"])
        st.dataframe(history_df, use_container_width=True)
        st.download_button(
            "Télécharger le portefeuille d'analyses (CSV)",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="analyses_itc.csv",
            mime="text/csv",
        )
    else:
        st.write("Aucune analyse enregistrée pour le moment.")


def render_methodology() -> None:
    with st.expander("À propos de la méthodologie"):
        st.markdown(
            """
            ### Hypothèses principales
            - Les taux de droits sont exprimés en pourcentage de la valeur en douane.
            - La valeur exportée est saisie en millions USD pour faciliter la lecture.
            - Le pass-through estime la part du tarif supportée par le client final.

            ### Sources et extensions possibles
            - Les données peuvent être remplacées par un fichier CSV actualisé (même structure) pour refléter de nouveaux secteurs.
            - L'outil peut être connecté à une base de données ITC ou à une API tarifaire pour une mise à jour automatique.
            - Ajouter une couche de simulation via l'élasticité-prix de la demande pour affiner l'impact volume.
            """
        )


def main() -> None:
    _init_session_state()

    tariff_df = load_tariff_data()
    market_df = load_market_data()

    display_header()
    render_overview(tariff_df)

    params = sidebar_inputs(tariff_df)
    metrics = compute_impacts(params)

    render_results(params, metrics)
    render_saved_scenarios(params, metrics)

    st.subheader("Cartographie des marchés alternatifs")
    st.dataframe(market_df, hide_index=True, use_container_width=True)

    render_methodology()


if __name__ == "__main__":
    main()
