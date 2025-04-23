import streamlit as st
import pandas as pd

# Load Excel data
@st.cache_data
def load_data():
    return pd.read_excel("quiz_data.xlsx")

df = load_data()
st.title("🍷 Quiz: Weinservice & Gastronomie")

score = 0
user_answers = []

df = df.sample(frac=1).reset_index(drop=True)

def render_question(row, index):
    st.markdown(f"### {index + 1}. {row['Question']}")
    qtype = row['Type']
    options = [row['Option 1'], row['Option 2'], row['Option 3'], row['Option 4']]
    options = [opt for opt in options if pd.notna(opt)]

    if qtype == "MCQ":
        return st.radio("Wählen Sie eine Antwort:", options, key=f"mcq_{index}")
    elif qtype == "Checkbox":
        return st.multiselect("Wählen Sie alle richtigen Antworten:", options, key=f"chk_{index}")
    elif qtype == "Matching":
        st.info("Bitte geben Sie die passende Zuordnung ein (z. B.: A → 1, B → 2)")
        return st.text_input("Ihre Zuordnung:", key=f"match_{index}")
    elif qtype == "Sequence":
        st.info("Bitte geben Sie die Reihenfolge ein (z. B.: 1–2–3–4–5)")
        return st.text_input("Reihenfolge:", key=f"seq_{index}")
    else:
        st.warning("Unbekannter Fragetyp")
        return ""

for i, row in df.iterrows():
    answer = render_question(row, i)
    user_answers.append((row['Correct Answer(s)'], answer))

if st.button("✅ Quiz auswerten"):
    for i, (correct, given) in enumerate(user_answers):
        st.markdown(f"#### Frage {i + 1}:")
        correct_str = str(correct).strip().lower()
        given_str = ', '.join(sorted(given)).lower() if isinstance(given, list) else str(given).strip().lower()
        if correct_str == given_str:
            st.success("✔️ Richtig")
            score += 1
        else:
            st.error(f"❌ Falsch – Richtige Antwort: {correct}")
    st.markdown(f"## 🧾 Ergebnis: {score} von {len(user_answers)} Punkten")
