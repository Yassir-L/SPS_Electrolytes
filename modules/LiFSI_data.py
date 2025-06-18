import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():
    st.title("🧪 Matières premières critiques – LiFSI")

    # 1. Hydroxyde de lithium
    st.markdown("### 1. Évolution du marché de l’hydroxyde de lithium en Chine (2015–2022)")
    data = pd.DataFrame({
        "Année": list(range(2015, 2023)),
        "Production": [2.2, 2.5, 3.5, 5, 7.6, 9.28, 17.5, 13.6],
        "Demande apparente": [1.28, 1.53, 1.69, 2.4, 2.78, 3.68, 10.5, 8.01],
        "Importations": [0.02, 0.01, 0.13, 0.13, 0.05, 0.05, 0.36, 0.24],
        "Exportations": [0.94, 0.98, 1.94, 2.73, 4.87, 5.66, 7.36, 5.83]
    })
    st.dataframe(data)

    fig1, ax1 = plt.subplots()
    ax1.bar(data["Année"], data["Production"], width=0.3, label="Production", align='center')
    ax1.bar(data["Année"], data["Demande apparente"], width=0.3, label="Demande", align='edge')
    ax2 = ax1.twinx()
    ax2.plot(data["Année"], data["Importations"], label="Importations", color="gray", linestyle="--", marker="o")
    ax2.plot(data["Année"], data["Exportations"], label="Exportations", color="orange", linestyle="--", marker="s")
    ax1.set_ylabel("Volume (10k t)")
    ax1.set_xlabel("Année")
    ax2.set_ylabel("Flux (10k t)")
    fig1.legend(loc="upper right")
    st.pyplot(fig1)

    # 2. Structure des coûts (oxychlorure de thionyle)
    st.markdown("### 2. Structure des coûts de l’oxyde de thionyle en Chine (2021)")
    cost_data = pd.DataFrame({
        "Composant": [
            "Chlore liquide (Cl2)", "Autres matières premières", "Dioxyde de soufre (SO2)",
            "Acide sulfurique (H2SO4)", "Coûts de fabrication", "Main-d'œuvre directe"
        ],
        "Part (%)": [43.7, 16.4, 14.9, 11.2, 11.2, 2.7]
    })
    st.dataframe(cost_data)

    fig2, ax2 = plt.subplots()
    ax2.pie(cost_data["Part (%)"], labels=cost_data["Composant"], autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

    # 3. Exportations d’acide chlorosulfonique
    st.markdown("### 3. Exportations chinoises d’acide chlorosulfonique (2017–2022)")
    chlorosulfonic = pd.DataFrame({
        "Année": [2017, 2018, 2019, 2020, 2021, 2022],
        "Volume exporté": [0.2939, 0.3022, 0.3252, 0.3627, 0.4158, 0.2966],
        "Prix moyen ($/t)": [350, 460.3, 391.9, 357.6, 376.9, 443.5]
    })
    st.dataframe(chlorosulfonic)

    fig3, ax3 = plt.subplots()
    ax3.bar(chlorosulfonic["Année"], chlorosulfonic["Volume exporté"], color='skyblue', label="Volume exporté")
    ax4 = ax3.twinx()
    ax4.plot(chlorosulfonic["Année"], chlorosulfonic["Prix moyen ($/t)"], color='orange', marker='o', label="Prix moyen")
    ax3.set_ylabel("Volume exporté (10k t)")
    ax4.set_ylabel("Prix moyen ($/t)")
    ax3.set_xlabel("Année")
    fig3.legend(loc="upper right")
    st.pyplot(fig3)

    # Tu peux ajouter les autres datasets ici : carbonate de lithium, acide sulfamique, prix mensuels...
