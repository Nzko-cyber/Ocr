from flask import Flask, request, jsonify
import os
import torch
from Ocr2.src.document_structure.extract_tables import extract_table_data
from Ocr2.src.document_structure.heading_paragraph_analysis import process_document

from Ocr2.src.ocr.easyocr_inference import ocr_with_easyocr
from Ocr2.src.ocr.multi_page_processing import process_pdf, process_docx
from Ocr2.src.classification.predict_category import load_model, predict_category
from Ocr2.src.extraction.extract_key_data import process_ocr_results
from Ocr2.src.extraction.spelling_punctuation_check import check_spelling_and_punctuation

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Глобальная загрузка модели
MODEL_PATH = "models/classifier_model.pth"
LABEL_CLASSES = ['advertisement', 'budget', 'email', 'file folder', 'form',
                 'handwritten', 'invoice', 'letter', 'memo', 'news article',
                 'questionnaire', 'resume', 'scientific publication', 'scientific report', 'specification']
EXECUTION_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CLASSIFICATION_MODEL = load_model(MODEL_PATH, num_classes=len(LABEL_CLASSES), execution_device=EXECUTION_DEVICE)


app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "OCR, Classification, and Extraction API is running!"})

@app.route("/classify", methods=["POST"])
def classify():

    file_path = request.json.get("file_path")

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid or missing file_path"}), 400

    try:
        category = predict_category(file_path, CLASSIFICATION_MODEL, EXECUTION_DEVICE, LABEL_CLASSES)
        return jsonify({"message": "Классификация завершена", "category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ocr", methods=["POST"])
def ocr():

    file_path = request.json.get("file_path")
    output_path = os.path.join(OUTPUT_FOLDER, "ocr_results")
    os.makedirs(output_path, exist_ok=True)

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid or missing file_path"}), 400

    try:
        if file_path.endswith(".pdf"):
            process_pdf(file_path, output_path)
        elif file_path.endswith(".docx"):
            process_docx(file_path, output_path)
        else:
            ocr_with_easyocr(os.path.dirname(file_path), output_path)

        return jsonify({"message": "OCR завершен", "output_path": output_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/spellcheck", methods=["POST"])
def spellcheck():

    ocr_results_dir = request.json.get("ocr_results_dir")
    output_dir = os.path.join(OUTPUT_FOLDER, "corrected_text")
    os.makedirs(output_dir, exist_ok=True)

    if not ocr_results_dir or not os.path.exists(ocr_results_dir):
        return jsonify({"error": "OCR results directory not found"}), 400

    try:
        check_spelling_and_punctuation(ocr_results_dir, output_dir)
        return jsonify({"message": "Проверка орфографии завершена", "output_path": output_dir}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract_tables", methods=["POST"])
def extract_tables():

    file_path = request.json.get("file_path")
    output_dir = os.path.join(OUTPUT_FOLDER, "tables")
    os.makedirs(output_dir, exist_ok=True)

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400

    try:
        extract_table_data(file_path, os.path.join(output_dir, "extracted_table.csv"))
        return jsonify({"message": "Таблица извлечена", "output_path": output_dir}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze_headings", methods=["POST"])
def analyze_headings():
    """
    Анализ заголовков и абзацев в документе.
    """
    file_path = request.json.get("file_path")
    output_dir = os.path.join(OUTPUT_FOLDER, "headings_paragraphs")

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400

    try:
        process_document(file_path, output_dir)
        return jsonify({"message": "Анализ заголовков завершен", "output_path": output_dir}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract", methods=["POST"])
def extract():
    """
    Извлекает ключевые данные из OCR результатов.
    """
    ocr_dir = request.json.get("ocr_results_dir")
    output_path = os.path.join(OUTPUT_FOLDER, "extracted_data")

    if not ocr_dir or not os.path.exists(ocr_dir):
        return jsonify({"error": "OCR results directory not found"}), 400

    try:
        process_ocr_results(ocr_dir, output_path)
        return jsonify({"message": "Извлечение данных завершено", "output_path": output_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
