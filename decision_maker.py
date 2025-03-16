# decision_maker.py
import memory
import random


def make_decision():
    memory_data = memory.load_memory()
    if "INSIGHTS" not in memory_data or not memory_data["INSIGHTS"]:
        print("🛑 Нет инсайтов для принятия решений.")
        return
    decision = random.choice(memory_data["INSIGHTS"])
    print(f"\n🤖 Аполлон принял решение: {decision}")
    with open("decision_log.txt", "a", encoding="utf-8") as log:
        log.write(f"Принятое решение: {decision}\n")
