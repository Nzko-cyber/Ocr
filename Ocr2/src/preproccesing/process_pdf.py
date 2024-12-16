import os
from pdf2image import convert_from_path

def process_pdf(input_dir, output_dir, dpi=300):
    """
    Конвертирует PDF-документы в изображения (одна страница - одно изображение).
    :param input_dir: Папка с PDF-файлами.
    :param output_dir: Папка для сохранения изображений.
    :param dpi: Качество выходного изображения (по умолчанию 300 dpi).
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file_name)
            print(f"Обрабатываю PDF: {pdf_path}")

            # Конвертация страниц PDF в изображения
            pages = convert_from_path(pdf_path, dpi=dpi)
            pdf_base_name = os.path.splitext(file_name)[0]

            for idx, page in enumerate(pages):
                image_path = os.path.join(output_dir, f"{pdf_base_name}_page_{idx+1}.jpg")
                page.save(image_path, "JPEG")
                print(f"Сохранено изображение: {image_path}")

if __name__ == "__main__":
    input_pdf_dir = "data/pdf_files"          # Папка с PDF-файлами
    output_image_dir = "data/processed_pdf"   # Папка для сохранения изображений

    process_pdf(input_pdf_dir, output_image_dir)
