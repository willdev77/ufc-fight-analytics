import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import joblib

# Padroziando o estilo
sns.set_style("whitegrid")

#Titulo da Pagina
st.set_page_config(
    page_title="UFC Analytics Dashboard",
    page_icon="🥊",
    layout="wide"
)

# ======================
# CORES UFC
# ======================

ufc_red = "#D20A0A"
ufc_black = "#0E0E0E"
ufc_gray = "#1F1F1F"

# ======================
# CSS (CARDS PROFISSIONAIS)
# ======================

st.markdown("""
<style>

.block-container{
padding-top:2rem;
}

.fighter-card{
background-color:#f5f5f5;
padding:20px;
border-radius:10px;
box-shadow:0px 2px 6px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

# ======================
# CARREGAR DADOS
# ======================
model = joblib.load("model/ufc_model.pkl")
df = pd.read_csv("data/Fights.csv")

# ======================
# HEADER
# ======================

st.markdown(
    "<h1 style='color:#D20A0A;'>🥊 UFC Fight Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

st.write("Dashboard interativo de análise de performance de lutadores")


# ======================
# FILTROS
# ======================
df_fighter1 = df[[
    "Fighter_1","Fighter_2",
    "Result_1",
    "Method","Method Details",
    "STR_1","KD_1","TD_1","Sub. Att_1",
    "Sig. Str. %_1",
    "Distance_%_1","Clinch_%_1","Ground_%_1"
]].copy()

df_fighter1 = df_fighter1.rename(columns={
    "Fighter_1":"Fighter",
    "Fighter_2":"Opponent",
    "Result_1":"Result",
    "STR_1":"STR",
    "KD_1":"KD",
    "TD_1":"TD",
    "Sub. Att_1":"SUB",
    "Sig. Str. %_1":"ACCURACY",
    "Distance_%_1":"DISTANCE",
    "Clinch_%_1":"CLINCH",
    "Ground_%_1":"GROUND"
})

df_fighter2 = df[[
    "Fighter_2","Fighter_1",
    "Result_2",
    "Method","Method Details",
    "STR_2","KD_2","TD_2","Sub. Att_2",
    "Sig. Str. %_2",
    "Distance_%_2","Clinch_%_2","Ground_%_2"
]].copy()

df_fighter2 = df_fighter2.rename(columns={
    "Fighter_2":"Fighter",
    "Fighter_1":"Opponent",
    "Result_2":"Result",
    "STR_2":"STR",
    "KD_2":"KD",
    "TD_2":"TD",
    "Sub. Att_2":"SUB",
    "Sig. Str. %_2":"ACCURACY",
    "Distance_%_2":"DISTANCE",
    "Clinch_%_2":"CLINCH",
    "Ground_%_2":"GROUND"
})

df_long = pd.concat([df_fighter1, df_fighter2])
fighters = sorted(df_long["Fighter"].unique())

# ======================
# SIDEBAR FILTROS
# ======================

st.sidebar.title("Filters")

fighter1 = st.sidebar.selectbox("Select Fighter 1", fighters, index=0)
fighter2 = st.sidebar.selectbox("Select Fighter 2", fighters, index=1)

# filtrar lutas do lutador (aparece em qualquer lado)
df_f1 = df_long[df_long["Fighter"] == fighter1]
df_f2 = df_long[df_long["Fighter"] == fighter2]

# dataframe combinado
df_compare = pd.concat([df_f1, df_f2])

# paleta de cores
ufc_palette = {
    fighter1: ufc_red,
    fighter2: ufc_black
}


# ======================
# dataframe combinado
# ======================

st.subheader("📊 Fighter Overview")

card1, card2 = st.columns(2)

with card1:

    wins1 = (df_f1["Result"] == "W").sum()
    losses1 = (df_f1["Result"] == "L").sum()
    draws1 = (df_f1["Result"] == "D").sum()

    st.markdown(f"""
    <div class="fighter-card">

    <h3>{fighter1}</h3>

    <b>Record:</b> {wins1}-{losses1}-{draws1}<br>
    <b>Fights:</b> {len(df_f1)}<br><br>

    <b>Avg Strikes:</b> {round(df_f1.STR.mean(),1)}<br>
    <b>Avg Knockdowns:</b> {round(df_f1.KD.mean(),2)}<br>
    <b>Avg Takedowns:</b> {round(df_f1.TD.mean(),2)}<br>
    <b>Avg Sub Attempts:</b> {round(df_f1.SUB.mean(),2)}

    </div>
    """, unsafe_allow_html=True)

with card2:

    wins2 = (df_f2["Result"]=="W").sum()
    losses2 = (df_f2["Result"]=="L").sum()
    draws2 = (df_f2["Result"]=="D").sum()

    st.markdown(f"""
    <div class="fighter-card">

    <h3>{fighter2}</h3>

    <b>Record:</b> {wins2}-{losses2}-{draws2}<br>
    <b>Fights:</b> {len(df_f2)}<br><br>

    <b>Avg Strikes:</b> {round(df_f2.STR.mean(),1)}<br>
    <b>Avg Knockdowns:</b> {round(df_f2.KD.mean(),2)}<br>
    <b>Avg Takedowns:</b> {round(df_f2.TD.mean(),2)}<br>
    <b>Avg Sub Attempts:</b> {round(df_f2.SUB.mean(),2)}

    </div>
    """, unsafe_allow_html=True)

# ======================
# PRIMEIRA LINHA (3 GRÁFICOS)
# ======================

c1, c2, c3 = st.columns(3)

with c1:

    st.subheader("Strike Distribution")

    fig, ax = plt.subplots()
    sns.histplot(
    data=df_compare,
    x="STR",
    hue="Fighter",
    bins=20,
    palette=ufc_palette,
    ax=ax
    ) 
    ax.set_xlabel("Strikes Landed per Fight")
    ax.set_ylabel("Number of Fights")

    st.pyplot(fig)

with c2:

    st.subheader("Strikes vs Knockdowns")

    fig, ax = plt.subplots()

    sns.scatterplot(
    data=df_compare,
    x="STR",
    y="KD",
    hue="Fighter",
    palette=ufc_palette,
    ax=ax
    )   

    ax.set_xlabel("Strikes Landed")
    ax.set_ylabel("Knockdowns")

    st.pyplot(fig)


with c3:

    st.subheader("Strike Accuracy")

    fig, ax = plt.subplots()

    sns.histplot(
    data=df_compare,
    x="ACCURACY",
    hue="Fighter",
    palette=ufc_palette,
    bins=30,
    alpha=0.6,
    ax=ax
    )

    ax.set_xlabel("Significant Strike Accuracy")
    ax.set_ylabel("Number of Fights")

    st.pyplot(fig)

# ======================
# SEGUNDA LINHA (3 GRÁFICOS)
# ======================

c4, c5, c6 = st.columns(3)

with c4:

    st.subheader("Fighting Style")

    style1 = df_f1[
    ["DISTANCE","CLINCH","GROUND"]
    ].mean()

    style2 = df_f2[
    ["DISTANCE","CLINCH","GROUND"]
    ].mean()

    style_df = pd.DataFrame({
    fighter1: style1,
    fighter2: style2
})

    fig, ax = plt.subplots()

    style_df.plot(
    kind="bar",
    ax=ax,
    color=[ufc_red, "black"]
    )

    ax.set_ylabel("Percentage")

    st.pyplot(fig)


with c5:

    st.subheader("Strike Efficiency")

    fig, ax = plt.subplots()


    sns.scatterplot(
    data=df_compare,
    x="STR",
    y="ACCURACY",
    hue="Fighter",
    palette=ufc_palette,
    s=120,
    ax=ax
    )   

    ax.set_xlabel("Strikes Landed per Fight")
    ax.set_ylabel("Strike Accuracy")

    st.pyplot(fig)


with c6:

    st.subheader("Knockdown Distribution")

    fig, ax = plt.subplots()

    sns.histplot(
    data=df_compare,
    x="KD",
    hue="Fighter",
    palette=ufc_palette,
    bins=20,
    alpha=0.6,
    ax=ax
    )

    ax.set_xlabel("Knockdowns per Fight")
    ax.set_ylabel("Number of Fights")

    st.pyplot(fig)

st.divider()


# ======================
# COMPARAÇÃO LADO A LADO
# ======================

g1, g2 = st.columns(2)

# ======================
# BAR COMPARISON
# ======================

with g1:

    st.subheader("Fighter Performance Comparison")

    metrics = ["STR","TD","KD","SUB"]
    labels = ["Strikes","Takedowns","Knockdowns","Sub Attempts"]

    # NORMALIZAÇÃO
    df_norm = df_long.copy()

    for col in metrics:
        df_norm[col] = (df_long[col] - df_long[col].min()) / (df_long[col].max() - df_long[col].min())

    # valores normalizados
    fighter1_values = df_norm[df_norm["Fighter"] == fighter1][metrics].mean().values
    fighter2_values = df_norm[df_norm["Fighter"] == fighter2][metrics].mean().values

    comparison_df = pd.DataFrame({
        fighter1: fighter1_values,
        fighter2: fighter2_values
    }, index=labels)

    fig, ax = plt.subplots(figsize=(5,4))

    comparison_df.plot(
        kind="bar",
        ax=ax,
        color=[ufc_red, ufc_black]
    )

    ax.set_ylabel("Relative Performance (Normalized)")
    ax.set_ylim(0,1)

    st.pyplot(fig)


# ======================
# RADAR CHART
# ======================

with g2:

    st.subheader("🥊 Fighter Skill Profile")

    df_long["CONTROL"] = df_long["CLINCH"] + df_long["GROUND"]

    metrics = ["STR","TD","KD","SUB","CONTROL"]

    labels = [
        "Striking",
        "Takedowns",
        "Knockdowns",
        "Submissions",
        "Control"
    ]

    df_norm = df_long.copy()

    for col in metrics:
        df_norm[col] = df_long[col].rank(pct=True)

    fighter1_stats = df_norm[df_norm["Fighter"] == fighter1][metrics].mean().tolist()
    fighter2_stats = df_norm[df_norm["Fighter"] == fighter2][metrics].mean().tolist()

    fighter1_stats += fighter1_stats[:1]
    fighter2_stats += fighter2_stats[:1]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, polar=True)

    ax.plot(angles, fighter1_stats, color=ufc_red, linewidth=2, label=fighter1)
    ax.fill(angles, fighter1_stats, color=ufc_red, alpha=0.25)

    ax.plot(angles, fighter2_stats, color=ufc_black, linewidth=2, label=fighter2)
    ax.fill(angles, fighter2_stats, color=ufc_black, alpha=0.25)

    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)

    plt.legend(loc="upper right")

    st.pyplot(fig)

# ======================
# SKILL COMPARISON (PRO STYLE)
# ======================

st.subheader("🥊 Skill Comparison")

metrics = {
    "Striking":"STR",
    "Takedowns":"TD",
    "Knockdowns":"KD",
    "Submissions":"SUB"
}

for skill, col in metrics.items():

    # calcular percentil no dataset
    p1 = df_long[col].rank(pct=True)[df_long["Fighter"]==fighter1].mean()
    p2 = df_long[col].rank(pct=True)[df_long["Fighter"]==fighter2].mean()

    st.markdown(f"### {skill}")

    c1, c2 = st.columns(2)

    with c1:
        st.write(f"**{fighter1}**")
        st.progress(float(p1))
        st.write(f"{round(p1*100)} %")

    with c2:
        st.write(f"**{fighter2}**")
        st.progress(float(p2))
        st.write(f"{round(p2*100)} %")

st.divider()

#Função de previsão

def predict_fight(f1, f2):

    stats1 = df_long[df_long["Fighter"] == f1][
        ["STR","TD","KD","SUB","ACCURACY","DISTANCE","CLINCH","GROUND"]
    ].mean()

    stats2 = df_long[df_long["Fighter"] == f2][
        ["STR","TD","KD","SUB","ACCURACY","DISTANCE","CLINCH","GROUND"]
    ].mean()

    p1 = model.predict_proba([stats1])[0][1]
    p2 = model.predict_proba([stats2])[0][1]

    total = p1 + p2

    p1 = p1 / total
    p2 = p2 / total

    return p1, p2

st.header("🧠 Fight Outcome Prediction")

p1, p2 = predict_fight(fighter1, fighter2)

c1, c2 = st.columns(2)

with c1:
    st.subheader(fighter1)
    st.progress(float(p1))
    st.write(f"Win Probability: {round(p1*100)}%")

with c2:
    st.subheader(fighter2)
    st.progress(float(p2))
    st.write(f"Win Probability: {round(p2*100)}%")