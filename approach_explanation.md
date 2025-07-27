# Approach Explanation

## 📌 Overview

This solution processes a set of input PDF documents along with a `persona.json` file describing:
- The **persona** (e.g., Travel Planner)
- The **job to be done** (e.g., Plan a trip)
- The list of **PDF files** to analyze

The goal is to automatically extract the most relevant section from each PDF that aligns with the given persona and job, and generate a structured `output.json` in the format specified.

---

## ⚙️ Key Steps

### 1️⃣ **Load Inputs**
- The app reads `/app/input/persona.json` which contains:
  - `persona`
  - `job_to_be_done`
  - List of PDF filenames.
- Each PDF is loaded from `/app/input/`.

---

### 2️⃣ **Combine Persona and Job**
- The `persona` and `job_to_be_done` are combined to create a **focus context**.
- This helps the NLP model understand what sections of the PDFs are relevant.

---

### 3️⃣ **Dynamic Keyword Extraction**
- Using `spaCy`, the solution extracts key **noun phrases** and **named entities** from the persona and job description.
- These dynamic keywords guide what kind of content to look for in the PDFs.

---

### 4️⃣ **Process PDF Pages**
- Each PDF is opened page by page using **PyMuPDF**.
- For every page:
  - Calculate semantic **similarity** with the persona/job using `spaCy`.
  - Add a bonus score if keywords appear in the page text.
- This scoring ensures pages with relevant context rank higher.

---

### 5️⃣ **Select Best Page**
- For each PDF, only the **top-ranked page** is chosen.
- This guarantees only one extracted section per input PDF.

---

### 6️⃣ **Smart Section Title**
- The solution scans lines from the chosen page.
- It uses simple rules to detect the best heading:
  - Ignores long paragraphs or short bullet points.
  - Prefers lines that match title case, uppercase, or contain keywords.
  - Gives a boost to lines near the top of the page.

---

### 7️⃣ **Create Final JSON**
- The output includes:
  - **Metadata** with input documents, persona, job, and timestamp.
  - **Extracted Sections** with document name, best title, importance rank, and page number.
  - **Subsection Analysis** with a snippet of the selected page text.

---

## ✅ Why It Works

- The solution is **domain-agnostic** — it uses only dynamic keywords, so it works for travel, food, business, or any other topic.
- It avoids hardcoding any topic-specific logic.
- It ensures output strictly matches the **Round 1B format** with correct JSON structure.

---

## 📂 Output

The final `output.json` is saved to `/app/output/output.json` for the evaluation system to pick up.

---

## ⚡ Technologies Used

- **Python 3**
- **PyMuPDF** — fast PDF parsing.
- **spaCy** — robust NLP for semantic similarity and keyword extraction.

---

## 🚀 Ready for Evaluation

The container works fully **offline**, does not use any network calls, and only requires the input folder with:
- `persona.json`
- The PDF files listed.

It automatically writes `output.json` in the correct format.

---

**This ensures the solution is robust, clean, and portable across different test scenarios.**
