# analyzer.py
import memory


def run_analysis():
    memory_data = memory.load_memory()
    print("\n📊 АНАЛИЗ ПАМЯТИ:")
    for category, entries in memory_data.items():
        print(f"\n📂 Категория: {category}")
        for i, entry in enumerate(entries, 1):
            print(f"  {i}. {entry}")
    print("\n✅ Анализ завершён.")
