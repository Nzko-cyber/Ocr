import easyocr
import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ocr_processing.log", mode='w', encoding='utf-8')
    ]
)

def process_image(reader, image_path, output_dir, contrast_ths=0.7, adjust_contrast=0.5):
    file_name = os.path.basename(image_path)
    try:
        logging.info(f"Начало обработки файла: {file_name}")
        results = reader.readtext(image_path, detail=0, contrast_ths=contrast_ths, adjust_contrast=adjust_contrast)

        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"file": file_name, "text": results}, f, ensure_ascii=False, indent=4)  # type: ignore

        logging.info(f"Успешная обработка файла: {file_name}, результат сохранен в {output_path}")
    except Exception as e:
        logging.error(f"Ошибка обработки файла {file_name}: {e}")

def ocr_with_easyocr(input_dir, output_dir, num_threads=4, contrast_ths=0.7, adjust_contrast=0.5):
    reader = easyocr.Reader(['en', 'ru'])
    os.makedirs(output_dir, exist_ok=True)

    image_files = [
        os.path.join(input_dir, file_name)
        for file_name in os.listdir(input_dir)
        if isinstance(file_name, str) and file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))
    ]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(process_image, reader, image_path, output_dir, contrast_ths, adjust_contrast)
            for image_path in image_files
        ]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Ошибка при выполнении потока: {e}")

if __name__ == "__main__":
    input_folder = "data/processed_train\train"
    output_folder = "output/ocr_results"

    ocr_with_easyocr(
        input_dir=input_folder,
        output_dir=output_folder,
        num_threads=8,
        contrast_ths=0.6,
        adjust_contrast=0.7
    )
