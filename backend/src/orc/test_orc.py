import easyocr
import re

# Инициализируем OCR для русского языка
reader = easyocr.Reader(['ru'])

def ocr_image(image_path: str):
    results = reader.readtext(image_path)
    return [(res[1], res[2]) for res in results]  # текст + уверенность

def parse_result(ocr_list):
    text = " ".join([t[0] for t in ocr_list])

    name_match = re.search(r"(?:Фамилия И\.О\.|Имя)[:\s]*([А-Я][а-яё]+\s+[А-Я]\.\s*[А-Я]\.)", text)
    name = name_match.group(1).strip() if name_match else None

    exercise_match = re.search(r"(?:Упражнение)[:\s]*([а-яА-ЯёЁ\s\d\-()]+)", text)
    exercise = exercise_match.group(1).strip() if exercise_match else None

    result_match = re.search(r"(?:Результат)[:\s]*([\d.,]+)\s*(\w+)", text)
    result_value = result_match.group(1) if result_match else None
    unit = result_match.group(2) if result_match else None

    return {
        "athlete": name,
        "exercise": exercise,
        "result": float(result_value) if result_value else None,
        "unit": unit
    }

# Путь к твоему фото (измени под себя):
image_path = "C:/Users/Admin/Desktop/testt.png"

# Запуск теста
if __name__ == "__main__":
    print(" Распознаём...")
    ocr_results = ocr_image(image_path)
    print("Результат OCR:")
    for line in ocr_results:
        print(line)

    print("\n Парсим результат...")
    parsed = parse_result(ocr_results)
    print("Распарсенные данные:")
    for k, v in parsed.items():
        print(f"{k}: {v}")