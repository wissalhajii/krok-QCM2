import fitz
import json
import re

pdf_path = "/Users/wissal/Documents/Krok 2 Stomatology (EN).pdf"

doc = fitz.open(pdf_path)

quiz = []

current_question = ""
current_options = {}
correct_answer = None


def is_question_line(text):
    return re.match(r"^\d+\.\s", text)


def is_option_line(text):
    return re.match(r"^[a-e]\.\s", text)


for page in doc:

    drawings = page.get_drawings()

    green_rects = []

    # récupérer zones vertes
    for d in drawings:
        if "fill" in d and d["fill"]:
            r, g, b = d["fill"]
            if g > 0.6 and g > r and g > b:
                for item in d["items"]:
                    if item[0] == "re":
                        green_rects.append(fitz.Rect(item[1]))

    blocks = page.get_text("dict")["blocks"]

    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                spans = line["spans"]

                line_text = "".join([s["text"] for s in spans]).strip()

                if not line_text:
                    continue

                line_rect = fitz.Rect(spans[0]["bbox"])

                # nouvelle question
                if is_question_line(line_text):

                    if current_question:
                        quiz.append({
                            "question": current_question.strip(),
                            "options": [current_options.get(k, "") for k in ["a", "b", "c", "d", "e"]],
                            "reponse_correcte": correct_answer
                        })

                    current_question = line_text
                    current_options = {}
                    correct_answer = None

                # réponses
                elif is_option_line(line_text):

                    letter = line_text[0]
                    option = line_text[3:]

                    current_options[letter] = option

                    # vérifier highlight vert
                    if any(line_rect.intersects(gr) for gr in green_rects):
                        correct_answer = letter

                else:
                    if current_options:
                        last = list(current_options.keys())[-1]
                        current_options[last] += " " + line_text
                    else:
                        current_question += " " + line_text


# dernière question
if current_question:
    quiz.append({
        "question": current_question.strip(),
        "options": [current_options.get(k, "") for k in ["a", "b", "c", "d", "e"]],
        "reponse_correcte": correct_answer
    })

doc.close()

# nettoyage final
clean_quiz = []

for q in quiz:
    options = [opt for opt in q["options"] if opt.strip() != ""]
    if len(options) >= 5:
        clean_quiz.append(q)

# sauvegarde
with open("quiz.json", "w", encoding="utf-8") as f:
    json.dump(clean_quiz, f, indent=4, ensure_ascii=False)

print(f"Questions extraites : {len(clean_quiz)}")