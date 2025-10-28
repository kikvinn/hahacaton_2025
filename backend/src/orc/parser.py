import re

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