import easyocr

def extract_numbers_easyocr(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_path, detail=0)
    numbers = []
    for item in results:
        for s in item.split():
            if s.isdigit():
                numbers.append(int(s))
    return numbers
