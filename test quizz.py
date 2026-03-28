import json

# Charger le quiz
with open("quiz.json", "r", encoding="utf-8") as f:
    quiz = json.load(f)

score = 0

for i, q in enumerate(quiz, 1):
    print(f"\nQuestion {i}: {q['question']}")
    
    # afficher options
    for idx, option in enumerate(q["options"]):
        print(f"{chr(97+idx)}. {option}")
    
    # réponse utilisateur
    answer = input("Votre réponse (lettre) : ").lower().strip()

    # validation
    if answer == q.get("reponse_correcte"):
        print("✅ Correct !")
        score += 1
    else:
        correct_letter = q.get("reponse_correcte")
        
        if correct_letter is not None:
            correct_index = ord(correct_letter) - 97
            correct_text = q["options"][correct_index]
            print(f"❌ Incorrect. Bonne réponse : {correct_letter}. {correct_text}")
        else:
            print("⚠️ Réponse correcte non détectée dans le JSON")

print(f"\n🎯 Quiz terminé ! Score : {score}/{len(quiz)}")
