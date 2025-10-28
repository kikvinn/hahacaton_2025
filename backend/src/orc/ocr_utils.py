import easyocr

reader = easyocr.Reader(['ru'])

def ocr_image(image_path: str):
    results = reader.readtext(image_path)
    return [(res[1], res[2]) for res in results]  # текст + уверенность