# Enhanced Lead Qualification Tool

This repository contains a Python-based lead qualification tool that enhances traditional scraping by combining website content extraction with LLM-powered analysis. It scrapes key company web pages, extracts textual digital footprints, and evaluates whether the lead is relevant using a Groq-powered LLaMA-3 model.

---

## 🔍 Features

- Scrapes high-signal pages: `about`, `careers`, `blog`, `news`, etc.
- Extracts paragraph-level website content using `BeautifulSoup`.
- Uses Groq API (with LLaMA-3 model) for fast and accurate B2B lead qualification.
- Provides a simple `Yes/No` output based on the quality and relevance of the lead.
- Outputs results in a clean DataFrame (CSV export-ready).

---

## ⚙️ Setup Instructions
Step 1 : Install the necessary libraries</br>
      <b>cmd</b> - pip install -r requirements.txt</br>
      <b>jupyter</b> - !pip install -r requirements.txt

Step 2 : Get a API_KEY from "groq.com"
Step 3 : Place your api key in place of "YOUR_API_KEY" in the initializing section

Step 4 : Run all cells [In case of jupyter or colab] or simply run the python file
