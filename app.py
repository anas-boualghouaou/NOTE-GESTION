import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from io import BytesIO

# =========================
# CONFIGURATION
# =========================
st.set_page_config(
    page_title="ENSA Safi • Gestion des notes",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).parent / "dataset.csv"
PASSWORD = "123456789"

# =========================
# STYLE
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102a43 0%, #163d5c 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        background: linear-gradient(135deg, #102a43, #1f6f8b);
        padding: 30px 35px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(16,42,67,.15);
    }

    .hero h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 800;
    }

    .hero p {
        margin: 8px 0 0;
        opacity: .88;
        font-size: 15px;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 5px 20px rgba(16,42,67,.07);
        border: 1px solid #e9eef5;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e9eef5;
        box-shadow: 0 5px 20px rgba(16,42,67,.06);
    }

    .metric-title {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        color: #102a43;
        font-size: 28px;
        font-weight: 800;
        margin-top: 5px;
    }

    .section-title {
        color: #102a43;
        font-size: 22px;
        font-weight: 800;
        margin: 25px 0 12px;
    }

    .login-box {
        max-width: 460px;
        margin: 80px auto;
        background: white;
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 15px 50px rgba(16,42,67,.12);
        border: 1px solid #e9eef5;
    }

    .small-note {
        color: #64748b;
        font-size: 12px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        df = pd.DataFrame(columns=[
            "id", "nom", "prenom", "classe", "module",
            "note", "coefficient", "semestre"
        ])
        df.to_csv(DATA_FILE, index=False)
        return df

    df = pd.read_csv(DATA_FILE)

    numeric_cols = ["note", "coefficient"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def save_data(df):
    df.to_csv(DATA_FILE, index=False)
    load_data.clear()


def logout():
    st.session_state.authenticated = False
    st.session_state.classe = None
    st.rerun()


# =========================
# LOGIN
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "classe" not in st.session_state:
    st.session_state.classe = None

if not st.session_state.authenticated:
    st.markdown("""
    <div class="login-box">
        <div style="text-align:center">
            <div style="font-size:55px">🎓</div>
            <h1 style="color:#102a43;margin-bottom:5px">ENSA Safi</h1>
            <p style="color:#64748b">Plateforme de gestion des notes</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        classe = st.selectbox(
            "Choisissez votre espace",
            ["CP1", "CP2"]
        )
        password = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="Entrez votre mot de passe"
        )

        submitted = st.form_submit_button(
            "Se connecter",
            use_container_width=True
        )

        if submitted:
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.session_state.classe = classe
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")

    st.markdown(
        '<p style="text-align:center;color:#94a3b8;margin-top:20px">'
        'ENSA Safi • Administration académique</p>',
        unsafe_allow_html=True
    )
    st.stop()

# =========================
# APP
# =========================
df = load_data()

classe = st.session_state.classe
df_classe = df[df["classe"].str.upper() == classe.upper()].copy()

# Sidebar
with st.sidebar:
    st.markdown("## 🎓 ENSA Safi")
    st.markdown("---")
    st.markdown(f"### Espace {classe}")
    st.caption("Gestionnaire des notes")

    page = st.radio(
        "Navigation",
        [
            "🏠 Tableau de bord",
            "📋 Notes",
            "➕ Ajouter une note",
            "📊 Analyse",
        ]
    )

    st.markdown("---")
    st.caption("Session professeur")
    if st.button("🚪 Déconnexion", use_container_width=True):
        logout()

# Header
st.markdown(f"""
<div class="hero">
    <h1>Gestion des notes — {classe}</h1>
    <p>Tableau de bord académique • ENSA Safi</p>
</div>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
if page == "🏠 Tableau de bord":

    students = df_classe["id"].nunique() if not df_classe.empty else 0
    notes_count = len(df_classe)
    average = df_classe["note"].mean() if not df_classe.empty else 0
    success_rate = (
        (df_classe["note"] >= 10).mean() * 100
        if not df_classe.empty else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, "👨‍🎓 Étudiants", students),
        (c2, "📝 Notes enregistrées", notes_count),
        (c3, "📈 Moyenne générale", f"{average:.2f}/20"),
        (c4, "✅ Taux de réussite", f"{success_rate:.1f}%"),
    ]

    for col, title, value in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    if not df_classe.empty:
        st.markdown('<div class="section-title">📊 Vue générale</div>',
                    unsafe_allow_html=True)

        left, right = st.columns(2)

        with left:
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.histplot(
                data=df_classe,
                x="note",
                bins=10,
                kde=True,
                ax=ax
            )
            ax.set_title("Distribution des notes")
            ax.set_xlabel("Note /20")
            ax.set_ylabel("Nombre d'étudiants")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with right:
            module_avg = (
                df_classe.groupby("module")["note"]
                .mean()
                .sort_values(ascending=False)
            )

            fig, ax = plt.subplots(figsize=(7, 4))
            sns.barplot(
                x=module_avg.values,
                y=module_avg.index,
                ax=ax
            )
            ax.set_title("Moyenne par module")
            ax.set_xlabel("Moyenne /20")
            ax.set_ylabel("")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    else:
        st.info("Aucune note n'est encore enregistrée pour cette classe.")

# =========================
# NOTES
# =========================
elif page == "📋 Notes":

    st.markdown('<div class="section-title">📋 Registre des notes</div>',
                unsafe_allow_html=True)

    if df_classe.empty:
        st.info("Aucune note disponible.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            search = st.text_input(
                "🔎 Rechercher",
                placeholder="Nom ou prénom..."
            )

        with col2:
            modules = ["Tous"] + sorted(df_classe["module"].dropna().unique().tolist())
            selected_module = st.selectbox("Module", modules)

        with col3:
            semester = st.selectbox(
                "Semestre",
                ["Tous", "S1", "S2"]
            )

        filtered = df_classe.copy()

        if search:
            mask = (
                filtered["nom"].astype(str).str.contains(search, case=False, na=False)
                | filtered["prenom"].astype(str).str.contains(search, case=False, na=False)
            )
            filtered = filtered[mask]

        if selected_module != "Tous":
            filtered = filtered[filtered["module"] == selected_module]

        if semester != "Tous":
            filtered = filtered[filtered["semestre"] == semester]

        st.dataframe(
            filtered[
                ["id", "nom", "prenom", "module",
                 "semestre", "note", "coefficient"]
            ],
            use_container_width=True,
            hide_index=True
        )

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Télécharger les résultats",
            csv,
            file_name=f"notes_{classe.lower()}.csv",
            mime="text/csv"
        )

# =========================
# ADD
# =========================
elif page == "➕ Ajouter une note":

    st.markdown('<div class="section-title">➕ Ajouter une note</div>',
                unsafe_allow_html=True)

    with st.form("add_note"):
        c1, c2 = st.columns(2)

        with c1:
            student_id = st.number_input(
                "ID étudiant",
                min_value=1,
                step=1
            )
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            module = st.text_input("Module")

        with c2:
            semestre = st.selectbox("Semestre", ["S1", "S2"])
            note = st.number_input(
                "Note /20",
                min_value=0.0,
                max_value=20.0,
                step=0.25
            )
            coefficient = st.number_input(
                "Coefficient",
                min_value=0.1,
                max_value=20.0,
                value=1.0,
                step=0.5
            )

        submit = st.form_submit_button(
            "💾 Enregistrer la note",
            use_container_width=True
        )

        if submit:
            new_row = pd.DataFrame([{
                "id": int(student_id),
                "nom": nom.strip(),
                "prenom": prenom.strip(),
                "classe": classe,
                "module": module.strip(),
                "note": note,
                "coefficient": coefficient,
                "semestre": semestre
            }])

            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Note enregistrée avec succès.")
            st.rerun()

# =========================
# ANALYSIS
# =========================
elif page == "📊 Analyse":

    st.markdown('<div class="section-title">📊 Analyse académique</div>',
                unsafe_allow_html=True)

    if df_classe.empty:
        st.info("Pas assez de données pour réaliser une analyse.")
    else:
        stats = df_classe["note"].describe()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Moyenne", f"{stats['mean']:.2f}")
        c2.metric("Médiane", f"{df_classe['note'].median():.2f}")
        c3.metric("Maximum", f"{stats['max']:.2f}")
        c4.metric("Minimum", f"{stats['min']:.2f}")

        st.markdown("### Performance par semestre")

        semester_avg = (
            df_classe.groupby("semestre")["note"]
            .mean()
            .reset_index()
        )

        fig, ax = plt.subplots(figsize=(9, 4))
        sns.barplot(
            data=semester_avg,
            x="semestre",
            y="note",
            ax=ax
        )
        ax.set_ylim(0, 20)
        ax.set_ylabel("Moyenne /20")
        ax.set_xlabel("Semestre")
        ax.set_title(f"Moyenne par semestre — {classe}")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("### Répartition réussite / échec")

        result = pd.Series({
            "Admis (≥ 10)": int((df_classe["note"] >= 10).sum()),
            "Non admis (< 10)": int((df_classe["note"] < 10).sum())
        })

        fig, ax = plt.subplots(figsize=(7, 4))
        result.plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        ax.set_title("Répartition des résultats")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

st.markdown("""
<div style="text-align:center;color:#94a3b8;padding:30px 0 10px">
    ENSA Safi • Plateforme de gestion des notes<br>
    <span style="font-size:11px">Application Streamlit</span>
</div>
""", unsafe_allow_html=True)
