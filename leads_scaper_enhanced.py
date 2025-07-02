import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36"
}

PAGES = ["", "about", "careers", "blog", "news"]

def get_page_text(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        text_blocks = soup.find_all("p")
        return ' '.join(p.get_text(strip=True) for p in text_blocks)
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return ""

def get_digital_footprint(domain):
    base_url = f"https://{domain.strip('/')}"
    all_text = []

    for path in PAGES:
        full_url = urljoin(base_url + "/", path)
        print(f"🌐 Scraping: {full_url}")
        page_text = get_page_text(full_url)
        if len(page_text) > 100:
            all_text.append(page_text)
        time.sleep(1.5)

    return '\n'.join(all_text)

"""## Initializing a pre trained model for analysis of footprints

Using groq to initialize a llm to identify whether a lead is good or not. It is fast and accurate because of NPU Technology
"""

from groq import Groq

def check_lead(sentence, industry):
    client = Groq(api_key="YOUR_API_KEY")

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert B2B lead qualification agent. Your task is to evaluate short text descriptions "
                    "and determine if they indicate a strong sales opportunity for a business-to-business product or service.\n\n"
                    "Only respond with one word:\n"
                    "- \"Yes\" → if it is a good lead (indicates interest, intent, or relevance)\n"
                    "- \"No\" → if it is not a good lead (irrelevant, non-commercial, or lacks buying intent)\n\n"
                    "Base your judgment on factors like business growth signals, interest in technology, hiring, expansion, "
                    "partnerships, or purchasing behavior.\n\n"
                    "Do not explain or justify your answer."
                    f"** Also make sure to add relevancy according to the their industry : {industry}**"
                )
            },
            {
                "role": "user",
                "content": sentence
            }
        ],
        temperature=0.2,
        max_tokens=1,
        top_p=1,
        stream=False
    )

    response = completion.choices[0].message.content.strip()
    return response

"""## Testing with demo company names

Testing with demo company names which can be replaced by the ones extracted by the SaaSquatch scraper tool and making the results in a DataFrame which can be easily merged with the table containing all the scraping results from the tool.
"""

import pandas as pd

industry = "Software development"
companies = ["freecodecamp.org", "oracle.com", "python.org"]

df = pd.DataFrame(columns=["company", "Good Lead ?"])

for company in companies:
    print(f"\n🔍 Fetching digital footprint for: {company}")
    footprint = get_digital_footprint(company)

    if footprint:
        print(f"\n✅ Extracted {len(footprint)} characters from {company}")
        print("="*60)
        lead_type = check_lead(footprint, industry)  # this should return "Yes" or "No"
    else:
        print("⚠️ No usable text found.\n")
        lead_type = "No data"

    df.loc[len(df)] = [company, lead_type]

print(df)