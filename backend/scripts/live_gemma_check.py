import os
import json
from dotenv import load_dotenv

# Load .env from project root or backend
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv()

from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont
import io

key = os.environ.get("GEMINI_API_KEY")
print(f"Key present: {bool(key)}")
client = genai.Client(api_key=key)

# 1. Test Text Notice Extraction
notice_text = """
*** CAMPUS ANNOUNCEMENT: CODE CRAFT HACKATHON 2026 ***
Organized by: Department of Computer Science & ITM Student Tech Club
Event Date: November 14-15, 2026
Registration Deadline: November 8, 2026 at 11:59 PM
Venue: Convention Hall B, ITM University Campus, Gwalior
Eligibility: All undergraduate and postgraduate students enrolled in recognized universities. Teams of 2 to 4 members.
Requirements: Bring valid university student ID card, personal laptop, and registration confirmation email. No registration fee required.
Action Items:
1. Form a team of 2-4 students.
2. Submit project proposal on portal.
3. Confirm Discord channel join.
Contact: techclub@itm.ac.in | +91 751 2456789
Note: Accommodation for outstation participants is subject to prior request by Nov 5.
"""

prompt = """
You are an expert campus information extraction assistant for CampusPulse AI.
Analyze the following campus announcement notice and extract structured information in JSON format.

Notice content:
""" + notice_text + """

You MUST output ONLY a valid JSON object matching this schema exactly:
{
  "title": "string or null",
  "category": "event | policy | academic | administrative | other",
  "summary": "concise overview string",
  "organizer": "string or null",
  "event_date": "string or null",
  "registration_deadline": "string or null",
  "venue": "string or null",
  "eligibility": ["string"],
  "requirements": ["string"],
  "important_dates": [{"label": "string", "date": "string"}],
  "action_items": [{"task": "string", "deadline": "string or null", "priority": "high | medium | low"}],
  "contact_information": [{"name_or_dept": "string", "contact": "string"}],
  "uncertainties": ["string - things that are unclear, ambiguous, or need verification"],
  "source_evidence": ["key quotes or facts directly from the notice"]
}
"""

print("\n--- 1. Testing Text Notice with gemma-4-26b-a4b-it ---")
response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)
print("Response text received:")
print(response.text)

parsed = json.loads(response.text)
print("Successfully parsed JSON keys:", list(parsed.keys()))

# 2. Test Image Notice Extraction
print("\n--- 2. Testing Image Poster with gemma-4-26b-a4b-it ---")
# Generate a test poster image with PIL
img = Image.new('RGB', (800, 600), color='#1E293B')
draw = ImageDraw.Draw(img)
draw.rectangle([(20, 20), (780, 580)], outline='#38BDF8', width=3)
draw.text((50, 50), "ANNUAL SCIENCE & TECH SYMPOSIUM 2026", fill='#F8FAFC')
draw.text((50, 110), "Organized by ITM Innovation Cell", fill='#94A3B8')
draw.text((50, 170), "Date: December 12, 2026 | Time: 10:00 AM", fill='#FDE047')
draw.text((50, 220), "Registration Closes: December 1, 2026", fill='#F87171')
draw.text((50, 270), "Venue: Main Auditorium, ITM University Gwalior", fill='#38BDF8')
draw.text((50, 330), "Eligibility: Open to all STEM students with min 60% aggregate", fill='#F8FAFC')
draw.text((50, 380), "Requirements: Submit 500-word abstract in PDF, Bring College ID", fill='#E2E8F0')
draw.text((50, 440), "Action: Register online at symposium.itm.ac.in before deadline", fill='#4ADE80')
draw.text((50, 500), "Contact: symposium@itm.ac.in | Room 302 Admin Block", fill='#94A3B8')

img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_bytes = img_byte_arr.getvalue()

image_prompt = """
Analyze this campus poster image and extract structured information into JSON following this schema:
{
  "title": "string or null",
  "category": "event | policy | academic | administrative | other",
  "summary": "concise overview",
  "organizer": "string or null",
  "event_date": "string or null",
  "registration_deadline": "string or null",
  "venue": "string or null",
  "eligibility": ["string"],
  "requirements": ["string"],
  "important_dates": [{"label": "string", "date": "string"}],
  "action_items": [{"task": "string", "deadline": "string or null", "priority": "high | medium | low"}],
  "contact_information": [{"name_or_dept": "string", "contact": "string"}],
  "uncertainties": ["string"],
  "source_evidence": ["string"]
}
Output only valid JSON.
"""

response_img = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents=[
        types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
        image_prompt
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)
print("Image Analysis Response text received:")
print(response_img.text)
parsed_img = json.loads(response_img.text)
print("Successfully parsed Image JSON keys:", list(parsed_img.keys()))
print("All Gemma 4 text and multimodal tests PASSED successfully!")
