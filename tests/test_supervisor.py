from agents.supervisor import classify_intent


questions = [
    "Can I take a 50000 rupee loan?",
    "Am I saving enough every month?",
    "Will I have enough money for my child's education?",
    "How much money will I need for retirement?",
    "How should I understand my investment risk?",
]


for question in questions:

    intent = classify_intent(question)

    print("\nQuestion:")
    print(question)

    print("Intent:")
    print(intent)