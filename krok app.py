import streamlit as st
import json

json_path = "/Users/wissal/quiz.json"

with open(json_path, "r", encoding="utf-8") as f:
    quiz = json.load(f)

st.set_page_config(page_title="Quiz Krok 2", page_icon="🧠", layout="centered")
st.title("🧠 Quiz Krok 2")

# session state
if "score" not in st.session_state:
    st.session_state.score = 0

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

if "result_message" not in st.session_state:
    st.session_state.result_message = None


def reset_quiz():
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.result_message = None


# sidebar
st.sidebar.title("Navigation")
go_to = st.sidebar.number_input(
    "Aller à la question",
    min_value=1,
    max_value=len(quiz),
    value=st.session_state.question_index + 1,
    step=1
)

if go_to - 1 != st.session_state.question_index:
    st.session_state.question_index = go_to - 1
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.result_message = None

st.sidebar.write(f"Total questions : {len(quiz)}")
st.sidebar.write(f"Score : {st.session_state.score}")

progress = (st.session_state.question_index + 1) / len(quiz)
st.sidebar.progress(progress)

if st.sidebar.button("🔄 Recommencer"):
    reset_quiz()
    st.rerun()

# fin du quiz
if st.session_state.question_index >= len(quiz):
    st.success(f"🎯 Score final : {st.session_state.score} / {len(quiz)}")
    if st.button("Recommencer le quiz"):
        reset_quiz()
        st.rerun()
    st.stop()

# question actuelle
q = quiz[st.session_state.question_index]

st.subheader(f"Question {st.session_state.question_index + 1}")
st.write(q["question"])

options = q["options"]

selected = st.radio(
    "Choisissez une réponse :",
    options,
    key=f"radio_{st.session_state.question_index}"
)

# validation
if st.button("Valider") and not st.session_state.answered:
    st.session_state.selected_answer = selected
    correct_letter = q.get("reponse_correcte")

    if correct_letter is None:
        st.session_state.result_message = ("warning", "⚠️ Réponse correcte non détectée dans le JSON")
    else:
        correct_index = ord(correct_letter) - 97

        if 0 <= correct_index < len(options):
            correct_text = options[correct_index]

            if selected == correct_text:
                st.session_state.score += 1
                st.session_state.result_message = ("success", "✅ Bonne réponse")
            else:
                st.session_state.result_message = (
                    "error",
                    f"❌ Mauvaise réponse\n\nBonne réponse : {correct_letter}. {correct_text}"
                )
        else:
            st.session_state.result_message = ("warning", "⚠️ Index de bonne réponse invalide")

    st.session_state.answered = True

# affichage résultat
if st.session_state.result_message:
    msg_type, msg_text = st.session_state.result_message
    if msg_type == "success":
        st.success(msg_text)
    elif msg_type == "error":
        st.error(msg_text)
    else:
        st.warning(msg_text)

# navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Précédent") and st.session_state.question_index > 0:
        st.session_state.question_index -= 1
        st.session_state.answered = False
        st.session_state.selected_answer = None
        st.session_state.result_message = None
        st.rerun()

with col2:
    if st.button("➡️ Suivant"):
        st.session_state.question_index += 1
        st.session_state.answered = False
        st.session_state.selected_answer = None
        st.session_state.result_message = None
        st.rerun()