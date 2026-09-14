from flask import Flask, request, jsonify
from rag import answer_question
import os
from ingestion import ingest_pdf

app = Flask(__name__)

@app.route("/ask", methods = ["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({
            "error": "Question is required"
        }), 400
    result = answer_question(question)
    return jsonify(result)

@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({
            "error": "PDF file is required"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400

    os.makedirs("data", exist_ok=True)

    pdf_path = os.path.join("data", "uploaded.pdf")

    file.save(pdf_path)

    pages, chunks = ingest_pdf(pdf_path)

    return jsonify({
        "message": "PDF uploaded successfully",
        "pages": pages,
        "chunks": chunks
    })

if __name__ == "__main__":
    app.run(debug = False)