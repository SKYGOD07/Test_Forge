"""
Gemma 4 Service for CampusPulse AI
Provides multimodal notice-to-action analysis using Gemma 4 via Google Gen AI SDK
"""

import json
import logging
import re
from typing import Optional, Dict, Any, List, Tuple
from google import genai
from google.genai import types

from ..config import Config

logger = logging.getLogger(__name__)

# Canonical schema structure
DEFAULT_SCHEMA = {
    "title": None,
    "category": "event",
    "summary": "",
    "organizer": None,
    "event_date": None,
    "registration_deadline": None,
    "venue": None,
    "eligibility": [],
    "requirements": [],
    "important_dates": [],
    "action_items": [],
    "contact_information": [],
    "uncertainties": [],
    "source_evidence": []
}

DEMO_SAMPLES = [
    {
        "id": "hackathon-gwalior",
        "title": "MLH Hack Day Gwalior x ITM University 2026",
        "category": "event",
        "badge": "Flagship Hackathon",
        "summary": "Official Hacktoberfest Hack Day organized at ITM University Gwalior in collaboration with Major League Hacking, featuring the Best Use of Gemma 4 prize category.",
        "organizer": "ITM University Gwalior x Major League Hacking (MLH)",
        "event_date": "October 24-25, 2026 (Starts 9:00 AM IST)",
        "registration_deadline": "October 20, 2026 at 11:59 PM IST",
        "venue": "Campus Convention Center, ITM University Gwalior, MP, India",
        "eligibility": [
            "Currently enrolled university or college students (undergraduate & graduate)",
            "Teams of 2 to 4 members permitted",
            "Individual registrations allowed (team matching provided at check-in)"
        ],
        "requirements": [
            "Valid College/University ID Card required at security desk",
            "Personal laptop and chargers",
            "Signed MLH Code of Conduct acknowledgment",
            "Prior registration confirmation QR code"
        ],
        "important_dates": [
            {"label": "Early Check-in & Team Matching", "date": "October 24, 2026 - 8:30 AM"},
            {"label": "Opening Keynote & Gemma 4 Briefing", "date": "October 24, 2026 - 10:00 AM"},
            {"label": "Hacking Period Starts", "date": "October 24, 2026 - 11:00 AM"},
            {"label": "Project Submission Deadline", "date": "October 25, 2026 - 12:00 PM"},
            {"label": "Judging & Award Ceremony", "date": "October 25, 2026 - 4:00 PM"}
        ],
        "action_items": [
            {"task": "Register your team on the official MLH event portal", "deadline": "October 20, 2026", "priority": "high"},
            {"task": "Join the official Discord hackathon announcements channel", "deadline": "October 22, 2026", "priority": "high"},
            {"task": "Set up your Google Gemini API key for the Gemma 4 prize category", "deadline": "October 23, 2026", "priority": "high"},
            {"task": "Bring government ID and university identity badge for gate entry", "deadline": "October 24, 2026", "priority": "medium"}
        ],
        "contact_information": [
            {"name_or_dept": "Organizing Committee", "contact": "hackday@itm.ac.in"},
            {"name_or_dept": "MLH Community Support", "contact": "discord.gg/mlh"}
        ],
        "uncertainties": [
            "Overnight campus hostel stay availability is subject to physical room allocation upon arrival.",
            "Hardware lab component requests must be verified with the lab technician at registration desk."
        ],
        "source_evidence": [
            "Event: MLH Hack Day Gwalior x ITM University",
            "Target Category: Best Use of Gemma 4 Prize",
            "Dates: October 24-25, 2026",
            "Location: ITM University Gwalior"
        ],
        "sample_text": "OFFICIAL ANNOUNCEMENT: MLH Hack Day Gwalior x ITM University 2026.\nJoin us on October 24-25, 2026 at ITM University Gwalior for an exciting 24-hour sprint. Compete for the Best Use of Gemma 4 prize! Registration closes October 20 at 11:59 PM. Teams of 2-4. Free entry, meals provided. Valid student ID required."
    },
    {
        "id": "exam-fee-notice",
        "title": "Fall Semester Examination Registration & Fee Schedule",
        "category": "administrative",
        "badge": "Academic Notice",
        "summary": "Mandatory examination enrollment notice for all semester 3, 5, and 7 engineering students. Requires clearance of semester tuition and online exam portal submission.",
        "organizer": "Office of the Controller of Examinations",
        "event_date": "Examinations commence: December 1, 2026",
        "registration_deadline": "November 15, 2026 (Without Late Fee)",
        "venue": "University Examination Hall & Online Portal (erp.itm.ac.in)",
        "eligibility": [
            "B.Tech / BCA / MCA students in Semesters 3, 5, and 7",
            "Minimum 75% attendance in all registered theory and lab courses",
            "No outstanding library fines or lab equipment dues"
        ],
        "requirements": [
            "Examination Fee: Rs. 2,500 payable via university ERP portal",
            "Uploaded passport-size photograph in student profile",
            "No Dues Clearance slip from respective department head"
        ],
        "important_dates": [
            {"label": "Standard Registration Deadline", "date": "November 15, 2026"},
            {"label": "Late Registration with Rs. 500 fine", "date": "November 20, 2026"},
            {"label": "Admit Card Generation Date", "date": "November 25, 2026"},
            {"label": "First Written Examination", "date": "December 1, 2026"}
        ],
        "action_items": [
            {"task": "Verify course codes and attendance percentage on student portal", "deadline": "November 10, 2026", "priority": "high"},
            {"task": "Pay examination fee of Rs. 2,500 via ERP gateway", "deadline": "November 15, 2026", "priority": "high"},
            {"task": "Download and print physical Admit Card after Nov 25", "deadline": "November 28, 2026", "priority": "medium"}
        ],
        "contact_information": [
            {"name_or_dept": "Examination Control Cell", "contact": "examcell@itm.ac.in | 0751-2459800"},
            {"name_or_dept": "ERP Helpdesk", "contact": "erphelp@itm.ac.in"}
        ],
        "uncertainties": [
            "Students with 70-74% attendance must submit medical certificates to Dean Academics by Nov 12.",
            "Practical viva examination dates will be published separately by individual departments."
        ],
        "source_evidence": [
            "Fee without fine: Nov 15, 2026",
            "Late fee window: Nov 16-20 with Rs 500 late fee",
            "Commencement: Dec 1, 2026",
            "75% attendance rule mandatory"
        ],
        "sample_text": "UNIVERSITY NOTICE: Examination Enrollment Fall 2026.\nStudents of 3rd, 5th, and 7th semesters must submit exam forms on erp.itm.ac.in by November 15, 2026. Regular fee: Rs. 2500. Late submissions accepted until Nov 20 with Rs. 500 fine. 75% attendance mandatory. Admit cards available Nov 25."
    },
    {
        "id": "campus-placement-drive",
        "title": "Google Cloud & AI Innovation Campus Placement Drive",
        "category": "academic",
        "badge": "Career Drive",
        "summary": "Campus recruitment drive for final year B.Tech/M.Tech computer science and engineering students for Cloud Engineer and AI Associate roles.",
        "organizer": "Central Training & Placement Cell (T&P)",
        "event_date": "November 18, 2026 at 9:30 AM",
        "registration_deadline": "November 12, 2026 at 5:00 PM",
        "venue": "Auditorium Block A & Placement Interview Suites",
        "eligibility": [
            "Final year B.Tech / M.Tech / MCA graduating in 2027",
            "CGPA 7.5 or above across all completed semesters",
            "No active backlogs allowed at the time of interview"
        ],
        "requirements": [
            "Three copies of updated resume in standardized format",
            "Formal business attire mandatory",
            "Original 10th, 12th, and semester grade sheets for verification",
            "Portfolio / GitHub link showcasing projects"
        ],
        "important_dates": [
            {"label": "Resume Submission Deadline", "date": "November 12, 2026 - 5:00 PM"},
            {"label": "Shortlist Announcement", "date": "November 14, 2026 - 6:00 PM"},
            {"label": "Online Aptitude & Coding Assessment", "date": "November 16, 2026 - 10:00 AM"},
            {"label": "On-Campus Technical & HR Interviews", "date": "November 18, 2026 - 9:30 AM"}
        ],
        "action_items": [
            {"task": "Submit updated resume and CGPA proof on T&P portal", "deadline": "November 12, 2026", "priority": "high"},
            {"task": "Review data structures, algorithms, and Gemini API fundamentals", "deadline": "November 15, 2026", "priority": "high"},
            {"task": "Prepare formal suit and bring 3 hard copies of resume", "deadline": "November 17, 2026", "priority": "medium"}
        ],
        "contact_information": [
            {"name_or_dept": "Training & Placement Officer", "contact": "tpo@itm.ac.in | Room 104 Admin"},
            {"name_or_dept": "Student Placement Coordinator", "contact": "+91 98765 43210"}
        ],
        "uncertainties": [
            "Exact package breakdown (fixed vs performance bonus) will be disclosed during Pre-Placement Talk.",
            "Work location (Bangalore / Hyderabad / Gurugram) assigned post-selection."
        ],
        "source_evidence": [
            "Eligible branches: CSE, IT, AI & Data Science",
            "Eligibility criteria: CGPA 7.5+",
            "Drive date: Nov 18, 2026",
            "Registration deadline: Nov 12, 2026"
        ],
        "sample_text": "PLACEMENT NOTICE: Tech Partner Campus Drive 2026.\nOpen to final year CS/IT students with CGPA 7.5+ and no backlogs. Positions: Associate AI Engineer. Apply on tpo portal by Nov 12, 5 PM. Online test Nov 16, In-person interviews Nov 18 in Auditorium A. Formal dress code strictly enforced."
    }
]


class GemmaAuthError(Exception):
    """Raised when GEMINI_API_KEY is not configured or invalid"""
    pass


class GemmaService:
    """Service to interact with Gemma 4 through the Gemini API"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.model = model or Config.GEMMA_MODEL or "gemma-4-26b-a4b-it"
        self._client: Optional[genai.Client] = None

    def _get_client(self) -> genai.Client:
        if not self.api_key:
            raise GemmaAuthError(
                "GEMINI_API_KEY is not configured on the server. "
                "Please configure GEMINI_API_KEY in your environment or use the preloaded Demo Mode."
            )
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    @property
    def is_configured(self) -> bool:
        """Check if GEMINI_API_KEY is configured"""
        return bool(self.api_key and self.api_key.strip())

    def get_status(self) -> Dict[str, Any]:
        """Return operational status and metadata"""
        return {
            "configured": self.is_configured,
            "model": self.model,
            "provider": "Google Gemini API",
            "engine": "Gemma 4",
            "multimodal_supported": True,
            "accepted_formats": ["png", "jpg", "jpeg", "webp", "text"]
        }

    def get_samples(self) -> List[Dict[str, Any]]:
        """Return pre-packaged demo samples for 1-click testing"""
        return DEMO_SAMPLES

    def analyze_notice(
        self,
        text: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        mime_type: Optional[str] = None,
        is_demo: bool = False,
        sample_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a campus notice using Gemma 4 or Demo Mode
        
        Args:
            text: Plain text extracted or provided from announcement
            image_bytes: Raw bytes of the notice/poster image
            mime_type: MIME type of the image (image/png, image/jpeg, image/webp)
            is_demo: Explicit flag to run demo mode
            sample_id: Specific sample ID if requested
            
        Returns:
            Normalized structured response dict
        """
        # 1. Handle Demo Mode
        if is_demo or not self.is_configured:
            if not is_demo and not self.is_configured:
                logger.info("GEMINI_API_KEY not configured; serving verified demo analysis")
            return self._build_demo_response(text=text, sample_id=sample_id)

        # 2. Validate Input
        if not text and not image_bytes:
            raise ValueError("Either notice text or a notice image must be provided.")

        client = self._get_client()

        # Build prompt instructions
        prompt = self._build_prompt(text_content=text)

        contents: List[Any] = []
        if image_bytes:
            clean_mime = mime_type or "image/png"
            if clean_mime not in {"image/png", "image/jpeg", "image/jpg", "image/webp"}:
                raise ValueError(f"Unsupported image format: {clean_mime}. Use PNG, JPEG, or WebP.")
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=clean_mime))

        contents.append(prompt)

        try:
            logger.info("Calling Gemma 4 (%s) with Gemini API...", self.model)
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )

            raw_text = response.text or ""
            logger.debug("Raw Gemma 4 response length: %d", len(raw_text))
            structured_data = self._parse_and_validate(raw_text)

            return {
                "success": True,
                "data": structured_data,
                "meta": {
                    "model": self.model,
                    "engine": "Gemma 4",
                    "mode": "live_gemini_api",
                    "has_image": bool(image_bytes),
                    "has_text": bool(text)
                }
            }

        except Exception as e:
            logger.error("Gemma 4 API request failed: %s", str(e), exc_info=True)
            # Safe sanitization of error message to protect any accidental credentials
            sanitized_err = re.sub(r'key=[A-Za-z0-9_\-]+', 'key=REDACTED', str(e))
            raise RuntimeError(f"Gemma 4 analysis failed: {sanitized_err}")

    def _build_prompt(self, text_content: Optional[str] = None) -> str:
        prompt = """
You are CampusPulse AI, an expert campus notice analysis assistant powered by Gemma 4.
Your mission is to transform messy campus announcements, event posters, and policy documents into clear, verified, actionable intelligence for university students and organizers.

CORE INSTRUCTIONS:
1. Extract ONLY facts explicitly supported by the supplied notice or image.
2. Differentiate between EVENT DATE and REGISTRATION DEADLINE accurately.
3. Identify all prerequisites, eligibility constraints, required documents, and entry fees.
4. If an item is unstated or ambiguous (e.g., missing submission portal URL, missing contact number, unclear fee), EXPLICITLY flag it in "uncertainties". Do NOT guess or invent contact details, URLs, or fees.
5. Create a prioritized action checklist (high / medium / low priority) that tells the student exactly what to do next.
6. Provide exact source quotes in "source_evidence" backing your extracted findings.

OUTPUT SCHEMA:
You MUST output ONLY a valid JSON object matching this schema exactly:
{
  "title": "string (Event or Notice Title)",
  "category": "event | policy | academic | administrative | career | other",
  "summary": "string (Concise 2-3 sentence overview)",
  "organizer": "string or null (Hosting club, department, or organization)",
  "event_date": "string or null (When the event happens)",
  "registration_deadline": "string or null (Hard cutoff deadline)",
  "venue": "string or null (Physical room/auditorium or virtual link)",
  "eligibility": ["string (Who can join or apply)"],
  "requirements": ["string (Required documents, laptop, fees, IDs)"],
  "important_dates": [
    {"label": "string", "date": "string"}
  ],
  "action_items": [
    {"task": "string", "deadline": "string or null", "priority": "high | medium | low"}
  ],
  "contact_information": [
    {"name_or_dept": "string", "contact": "string"}
  ],
  "uncertainties": [
    "string (Crucial facts missing, vague deadlines, or details requiring official verification)"
  ],
  "source_evidence": [
    "string (Direct quotes from the notice validating the extracted facts)"
  ]
}
"""
        if text_content:
            prompt += f"\nADDITIONAL TEXT NOTICE CONTENT:\n\"\"\"\n{text_content.strip()}\n\"\"\"\n"

        return prompt

    def _parse_and_validate(self, raw_text: str) -> Dict[str, Any]:
        """Clean markdown wrapping and validate schema"""
        cleaned = re.sub(r'<think>[\s\S]*?</think>', '', raw_text).strip()
        cleaned = cleaned.lstrip("\ufeff")
        cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\n?```\s*$', '', cleaned).strip()

        try:
            data = json.loads(cleaned)
        except Exception:
            # Bounded regex repair attempt
            json_match = re.search(r'(\{[\s\S]*\})', cleaned)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                except Exception as e:
                    raise ValueError(f"Model returned invalid JSON: {str(e)}")
            else:
                raise ValueError("Could not extract valid JSON from model response.")

        if not isinstance(data, dict):
            raise ValueError("Model output must be a top-level JSON dictionary.")

        # Normalize schema against defaults
        normalized = dict(DEFAULT_SCHEMA)
        for key in DEFAULT_SCHEMA:
            if key in data and data[key] is not None:
                normalized[key] = data[key]

        # Ensure lists are strictly lists
        for list_key in ["eligibility", "requirements", "important_dates", "action_items", "contact_information", "uncertainties", "source_evidence"]:
            if not isinstance(normalized.get(list_key), list):
                normalized[list_key] = [] if normalized.get(list_key) is None else [str(normalized[list_key])]

        return normalized

    def _build_demo_response(self, text: Optional[str] = None, sample_id: Optional[str] = None) -> Dict[str, Any]:
        """Provide a rich, pre-validated demo response matching one of our campus samples"""
        sample = None
        if sample_id:
            for s in DEMO_SAMPLES:
                if s["id"] == sample_id:
                    sample = s
                    break

        if not sample:
            # Pick best match based on keywords in text or default to MLH Hackathon
            if text:
                low = text.lower()
                if "exam" in low or "fee" in low:
                    sample = DEMO_SAMPLES[1]
                elif "placement" in low or "career" in low or "job" in low or "interview" in low:
                    sample = DEMO_SAMPLES[2]
                else:
                    sample = DEMO_SAMPLES[0]
            else:
                sample = DEMO_SAMPLES[0]

        data = {
            "title": sample["title"],
            "category": sample["category"],
            "summary": sample["summary"],
            "organizer": sample["organizer"],
            "event_date": sample["event_date"],
            "registration_deadline": sample["registration_deadline"],
            "venue": sample["venue"],
            "eligibility": sample["eligibility"],
            "requirements": sample["requirements"],
            "important_dates": sample["important_dates"],
            "action_items": sample["action_items"],
            "contact_information": sample["contact_information"],
            "uncertainties": sample["uncertainties"],
            "source_evidence": sample["source_evidence"],
        }

        return {
            "success": True,
            "data": data,
            "meta": {
                "model": self.model,
                "engine": "Gemma 4",
                "mode": "demo_simulation",
                "sample_id": sample["id"],
                "notice": "Demo Mode: Pre-verified CampusPulse AI sample. To run live inference, ensure GEMINI_API_KEY is active."
            }
        }
