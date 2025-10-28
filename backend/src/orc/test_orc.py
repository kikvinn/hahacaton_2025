
import base64
import requests
import json
import pandas as pd
import re

OPENROUTER_API_KEY = "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"

def analyze_table_image_with_openrouter(image_path: str) -> pd.DataFrame:
    print("[+] Подготовка запроса к OpenRouter...")

    # 1. Кодируем изображение в Base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # 2. Формируем запрос
    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Проанализируй эту таблицу результатов соревнований. "
                            "Для каждого участника извлеки следующие поля:\n"
                            "- ФИО (полное)\n"
                            "- Возраст (число)\n"
                            "- Пол (М/Ж)\n"
                            "- Вид спорта\n"
                            "- Дисциплина\n"
                            "- Результат (число)\n"
                            "- Единица измерения (секунды, метры и т.д.)\n"
                            "- Дата проведения (формат DD.MM.YYYY)\n"
                            "Верни строго массив JSON-объектов между ```json и ```, без пояснений и текста вне JSON. "
                            "Например: ```json [...] ```"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": 10000
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "TableParser"
    }

    print("[+] Отправка запроса в OpenRouter...")
    response = requests.post(url, json=payload, headers=headers)

    try:
        result = response.json() # Преобразование ответа в JSON <- ЗДЕСЬ
        content = result["choices"][0]["message"]["content"]

        #  Извлечение JSON из блока ```json ... ```
        match = re.search(r"```json\s*(\[[\s\S]*?\])\s*```", content)
        if match:
            json_str = match.group(1)
            parsed_data = json.loads(json_str)
            df = pd.DataFrame(parsed_data)
            print("[+] Данные успешно структурированы!")
            return df
        else:
            raise ValueError("Не удалось найти блок JSON в ответе модели.")
    except Exception as e:
        print(f"[!] Ошибка при парсинге ответа: {e}")
        print("Ответ модели:", response.text)
        return pd.DataFrame()

if __name__ == "__main__":
    image_path = "testt.jpg"  #ПУТЬ_К_ИЗОБРАЖЕНИЮ по запросу
    structured_df = analyze_table_image_with_openrouter(image_path)
    print(structured_df)