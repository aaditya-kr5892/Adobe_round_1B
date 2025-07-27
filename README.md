# 📄 Persona-Based PDF Section Extractor

This project automatically processes input PDF documents and extracts the most relevant section from each file based on a given **persona** and **job description**.  
It is designed to run fully offline inside a Docker container.

---

## 📌 **Folder Structure**
```
├── input/ # Mounted input folder
│ ├── persona.json 
│ ├── *.pdf # The PDF files listed in persona.json
├── output/ # Generated output.json will appear here
├── Dockerfile
├── main.py
├── requirements.txt
├── README.md
└── approach_explanation.md
```
---

## ⚙️ **How It Works**

1. The container reads `/app/input/persona.json` to get:
   - The **persona** (e.g., "Travel Planner")
   - The **job to be done** (e.g., "Plan a 4-day trip")
   - The list of input PDFs

2. For each PDF:
   - Uses NLP (spaCy) to calculate semantic similarity between pages and the persona/job context.
   - Extracts dynamic keywords from the persona/job to boost relevance scoring.
   - Picks **one best page**.
   - Detects the best heading/title line from that page.

3. Generates `output.json` in `/app/output` with:
   - Metadata
   - Extracted Sections
   - Subsection Analysis

---

## 🚀 **Build & Run**

### 1️⃣ **Build the Docker image**

```bash
docker build --platform linux/amd64 -t persona_extractor:latest .
```
### 2️⃣ **Run the container**
```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none persona_extractor:latest
```
- Input: Mounts your local input/ folder to /app/input inside the container.
- Output: Saves output.json to your local output/ folder.

## ✅ Requirements
- Docker (should support --platform linux/amd64)
- Local test files:
    - persona.json
    - PDFs listed inside persona.json

`Note:`
The input file must be named persona.json when mounted inside the container this is required for correct execution.
## 📂 Output
The generated output.json will match the format required by the challenge:
```bash
{
  "metadata": {...},
  "extracted_sections": [...],
  "subsection_analysis": [...]
}
```
## ⚡ Technologies Used
- Python 3
- spaCy for NLP similarity & keyword extraction
- PyMuPDF (fitz) for PDF text parsing