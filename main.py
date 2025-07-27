import os
import json
import fitz  # PyMuPDF
import spacy
import re
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def load_persona():
    persona_file = os.path.join(INPUT_DIR, "persona.json")
    with open(persona_file, "r") as f:
        data = json.load(f)
    persona = data["persona"]["role"]
    job = data["job_to_be_done"]["task"]
    documents = [doc["filename"] for doc in data["documents"]]
    return persona, job, documents

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        pages.append({"page_num": page_num, "text": text})
    return pages

def extract_focus_keywords(persona_text):
    doc = nlp(persona_text)
    keywords = set()
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2:
            keywords.add(chunk.text.lower())
    for ent in doc.ents:
        keywords.add(ent.text.lower())
    return list(keywords)

def rank_sections(pages, persona_job_text, focus_keywords):
    scores = []
    persona_doc = nlp(persona_job_text)

    for page in pages:
        page_doc = nlp(page["text"])
        similarity = persona_doc.similarity(page_doc)

        keyword_bonus = 0
        page_lower = page["text"].lower()
        for kw in focus_keywords:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', page_lower):
                keyword_bonus += 0.1

        scores.append({
            "page_number": page["page_num"],
            "text": page["text"],
            "similarity": similarity + keyword_bonus
        })

    ranked = sorted(scores, key=lambda x: x["similarity"], reverse=True)
    return ranked

def find_best_heading(page_text, focus_keywords):
    lines = page_text.split("\n")
    best_heading = "Untitled Section"
    best_score = 0

    for idx, line in enumerate(lines):
        line = line.strip()
        if len(line) < 5 or not any(c.isalpha() for c in line):
            continue

        if len(line.split()) > 15:
            continue

        if line.endswith("."):
            continue

        score = 0

        # Titlecase or uppercase boost
        if line == line.title() or line.isupper():
            score += 1

        # Keyword match boost
        lower_line = line.lower()
        for kw in focus_keywords:
            if kw.lower() in lower_line:
                score += 2

        # Top-of-page lines get boost
        if idx < 5:
            score += 1

        if score > best_score:
            best_heading = line
            best_score = score

    return best_heading

def main():
    persona, job, doc_filenames = load_persona()
    persona_text = persona + " " + job

    # Extract dynamic keywords from persona/job
    focus_words = extract_focus_keywords(persona_text)

    extracted_sections = []
    subsection_analysis = []

    for filename in doc_filenames:
        pdf_path = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(pdf_path):
            print(f"Warning: {filename} not found in input/")
            continue

        pages = extract_text(pdf_path)
        ranked = rank_sections(pages, persona_text, focus_words)

        # Pick only top ranked page
        best = ranked[0]

        # Improved heading detection
        section_title = find_best_heading(best["text"], focus_words)

        extracted_sections.append({
            "document": filename,
            "section_title": section_title,
            "importance_rank": len(extracted_sections) + 1,
            "page_number": best["page_number"]
        })

        snippet = best["text"][:500].replace("\n", " ")
        subsection_analysis.append({
            "document": filename,
            "refined_text": snippet,
            "page_number": best["page_number"]
        })

    output = {
        "metadata": {
            "input_documents": doc_filenames,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Output written to {output_file}")

if __name__ == "__main__":
    main()
