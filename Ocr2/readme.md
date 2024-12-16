OCR, Document Classification, and Data Extraction System
Project Overview
This project is a robust solution for:

Optical Character Recognition (OCR): Extracting text from various document formats (PDF, DOCX, JPG, etc.).
Document Classification: Automatically classifying documents into categories (e.g., invoices, letters, memos, etc.).
Key Data Extraction: Extracting critical information like dates, amounts, and names.
Spellcheck and Punctuation Correction: Fixing errors in OCR-processed text.
Document Structure Analysis: Retaining elements such as tables, headings, and paragraphs.
The system supports API endpoints for seamless integration into existing workflows and is optimized for high performance.

Key Features
High-Quality OCR:

Supports image and document formats like PDF, DOCX, and JPG.
Handles low-quality images using preprocessing (noise removal, sharpening).
Document Classification:

Classifies documents into predefined categories using a ResNet18-based classifier.
Predefined categories include invoices, letters, memos, and more.
Key Data Extraction:

Extracts structured information like sums, dates, and entity names.
Spellcheck and Correction:

Uses LanguageTool to correct spelling and punctuation errors.
Scalable API Integration:

RESTful API for document processing, OCR, classification, and extraction.
Project Structure
bash
Копировать код
project_root/
│
├── data/                             # Input data (train/val/test)
│   ├── processed_train/              # Preprocessed training data
│   ├── test/                         # Test data
│   └── ...
│
├── models/                           # Trained models
│   ├── classifier_model.pth          # Classification model
│   └── ner_model.pth                 # NER model (optional)
│
├── src/                              # Source code
│   ├── api/                          # API endpoints
│   │   └── app.py                    # Main Flask API
│   │
│   ├── classification/               # Document classification
│   │   ├── train_classifier.py       # Training classification model
│   │   └── predict_category.py       # Inference for classification
│   │
│   ├── document_structure/           # Document structure analysis
│   │   ├── extract_tables.py         # Table extraction
│   │   ├── heading_paragraph_analysis.py # Headings/paragraphs analysis
│   │   └── layout_analysis.py
│   │
│   ├── extraction/                   # Data extraction modules
│   │   ├── extract_key_data.py       # Key data extraction
│   │   └── spelling_punctuation_check.py # Spellcheck and correction
│   │
│   ├── ocr/                          # OCR modules
│   │   ├── easyocr_inference.py      # EasyOCR for text recognition
│   │   └── multi_page_processing.py  # PDF/DOCX multi-page processing
│   │
│   ├── preprocessing/                # Image preprocessing
│   │   ├── enhance_image.py          # Image enhancement
│   │   ├── process_pdf.py            # PDF processing
│   │   └── process_docx.py           # DOCX processing
│
├── test/                             # Tests for integration
│   └── test_integration.py
│
├── requirements.txt                  # Dependencies
└── README.md                         # Project documentation
Setup Instructions
1. Prerequisites
Ensure you have the following installed:

Python 3.8+
pip (Python package manager)
2. Installation
Clone the repository:

bash
Копировать код
git clone https://github.com/your-repo/ocr-document-system.git
cd ocr-document-system
Install dependencies:

bash
Копировать код
pip install -r requirements.txt
Create necessary folders:

bash
Копировать код
mkdir uploads output models
3. Running the Project
Start the API
Launch the Flask API server:

bash
Копировать код
python src/api/app.py
The API will be available at: http://127.0.0.1:5000

4. API Endpoints
1. Upload and Preprocess Documents
Endpoint: /api/preprocess
Method: POST
Request Body:
json
Копировать код
{
    "input_dir": "data/raw",
    "output_dir": "data/processed"
}
2. Perform OCR
Endpoint: /ocr
Method: POST
Request Body:
json
Копировать код
{
    "file_path": "uploads/sample.pdf"
}
3. Classify Documents
Endpoint: /classify
Method: POST
Request Body:
json
Копировать код
{
    "file_path": "uploads/sample_image.jpg"
}
4. Spellcheck and Correct
Endpoint: /spellcheck
Method: POST
Request Body:
json
Копировать код
{
    "ocr_results_dir": "output/ocr_results"
}
5. Extract Tables
Endpoint: /extract_tables
Method: POST
Request Body:
json
Копировать код
{
    "file_path": "uploads/sample_image.jpg"
}
5. Testing the Project
Run integration tests:

bash
Копировать код
python test/test_integration.py
6. Training the Models
Document Classification Model
To train the ResNet18 classification model:

bash
Копировать код
python src/classification/train_classifier.py
The model will be saved as models/classifier_model.pth.

Technologies Used
Frameworks: Flask, PyTorch, EasyOCR
Libraries: OpenCV, Pillow, scikit-learn, language-tool-python
Data Processing: JSON, pandas
Deployment: Flask (for API)
7. Future Improvements
Support additional document formats.
Enhance accuracy using custom OCR models.
Build a user-friendly frontend for API interaction.
8. Contact
For any issues or contributions, please create a pull request or contact:

Please pay attention to the file paths in the code
IDE:PYCHARM
dataset must be a at the src level: you can find dataset :https://github.com/Nzko-cyber/Ocr/pulls 