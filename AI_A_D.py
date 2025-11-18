# ======================================================
#  AI TEXT ANALYZER VS DETETKTOR |   Startup
#  Maqsad: Matnni tozalash, tahlil qilish va yaxshilash tavsiyalarini berish
# ======================================================

import re
import statistics
from collections import Counter
import matplotlib.pyplot as plt

# ===  MATNNI TOZALASH FUNKSIYASI ===
def clean_text(text):
    """
    Matndan keraksiz belgilarni (001, 01, control chars, zero-width) olib tashlaydi.
    """
    # Zero-width va control belgilarni olib tashlash
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    # 01 va 001 ketma-ketliklarini olib tashlash
    text = re.sub(r'(?:0{0,2}1{1,3})+', '', text)
    # Ortiqcha bo‘sh joylarni tozalash
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ===  MATN XUSUSIYATLARINI TAHLIL QILISH ===
def analyze_text_features(text):
    """
    Matnning burstiness, lexical diversity va repetition darajasini hisoblaydi.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentence_lengths = [len(s.split()) for s in sentences if s]
    avg_len = statistics.mean(sentence_lengths) if sentence_lengths else 0
    std_len = statistics.stdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
    burstiness = std_len / avg_len if avg_len > 0 else 0

    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    unique_words = len(set(words))
    lexical_diversity = unique_words / total_words if total_words else 0

    # So‘zlarning takrorlanish darajasi
    repetition_ratio = 1 - lexical_diversity

    analysis = {
        "Average sentence length": round(avg_len, 2),
        "Burstiness (std/avg)": round(burstiness, 3),
        "Lexical diversity": round(lexical_diversity, 3),
        "Repetition ratio": round(repetition_ratio, 3),
        "Sentence count": len(sentences),
        "Word count": total_words
    }
    return analysis


# ===  YAXSHILASH TAVSIYALARI ===
def suggest_improvements(analysis):
    """
    Tahlil natijalari asosida tavsiyalar beradi.
    """
    suggestions = []

    if analysis["Burstiness (std/avg)"] < 0.3:
        suggestions.append("👉 Gap uzunliklarini biroz farqlang — ritmni jonlantiring.")
    if analysis["Lexical diversity"] < 0.45:
        suggestions.append("👉 So‘z xilma-xilligini oshiring — sinonimlardan foydalaning.")
    if analysis["Repetition ratio"] > 0.5:
        suggestions.append("👉 Bir xil so‘zlarni kamroq takrorlang.")
    if analysis["Average sentence length"] > 25:
        suggestions.append("👉 Ba’zi gaplarni qisqartiring, o‘qish osonroq bo‘ladi.")
    if not suggestions:
        suggestions.append("✅ Matn tabiiy va balansli ko‘rinadi!")

    return suggestions


# ===  GRAFIK CHIZISH (Colab uchun chiroyli chiqadi) ===
def visualize_analysis(analysis):
    labels = list(analysis.keys())[:4]
    values = list(analysis.values())[:4]
    plt.figure(figsize=(7,4))
    plt.bar(labels, values)
    plt.title("Matn xususiyatlari tahlili", fontsize=14)
    plt.xticks(rotation=20)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.show()


# ===  FOYDALANISH (bu yerga matningizni yozing) ===
text = """
ushbu joyga matin AI dan matin tashlang.
"""

# ===  ISHLATISH JARAYONI ===
cleaned = clean_text(text)
analysis = analyze_text_features(cleaned)
suggestions = suggest_improvements(analysis)

print("🧹 Tozalangan matn:\n", cleaned)
print("\n📊 Tahlil natijalari:")
for k, v in analysis.items():
    print(f"  {k}: {v}")

print("\n💡 Yaxshilash tavsiyalari:")
for s in suggestions:
    print(" ", s)

visualize_analysis(analysis)
