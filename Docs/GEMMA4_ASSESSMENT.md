# CampusPulse AI: Best Use of Gemma 4 — Project Assessment

**Assessment date:** 16 October 2026  
**Status:** Pre-build assessment of the renamed repository; not evidence of a completed Gemma 4 integration.

## 1. Executive verdict

CampusPulse AI is a plausible foundation for the **Best Use of Gemma 4** challenge, but the current repository is **not submission-ready for that category**. It is currently a renamed, planning-stage fork of MiroFish: a broad multi-agent simulation application with a Python/Flask backend, Vue frontend, an OpenAI-SDK-compatible model wrapper, Zep Cloud graph memory, and OASIS-backed social simulation.

The published challenge brief asks for a focused experience that converts information in an image, screenshot, document, diagram, or other input into a useful result with Gemma 4. It specifies meaningful Gemma 4 use through the Gemini API, multimodal capability where it adds value, one clear user story, an end-to-end prototype, and a Gemma-powered result that is obvious within the first 30 seconds of the demo. The brief frames the build as a two-hour Hack Day challenge [1].

**Recommendation:** Keep the name **CampusPulse AI**, but narrow the first demo to **CampusPulse Notice-to-Action**: a student uploads a campus event poster, policy notice, or announcement screenshot; Gemma 4 extracts the facts, clearly marks what is missing or ambiguous, and produces an actionable checklist. The existing multi-agent simulator should remain a later extension, not a dependency for the first demo.

The current code has useful infrastructure to reuse, but it does not yet implement the required Gemma 4 API call or image-first interaction. Rebranding alone does not satisfy the prize.

## 2. Proposed project definition

### Name
**CampusPulse AI — Campus Notice-to-Action and Decision Intelligence**

### One-line pitch
Turn confusing campus notices into a reliable, evidence-conscious checklist of what a student needs to know and do.

### Primary user story
“As a university student, when I receive a dense event poster or campus notice, I want to upload a screenshot and immediately understand the deadline, eligibility, venue, required documents, registration path, and next actions—without manually decoding the entire notice.”

### First-demo input and output

**Input:** One PNG/JPEG screenshot of a campus announcement or event poster. Text/PDF input can follow once the image-first path is reliable.

**Output:**
- Event or notice title and category.
- Event date, registration deadline, time, and venue, when explicitly present.
- Eligibility rules and any team-size requirement.
- Required documents or prerequisites.
- Registration link/contact details, when visible.
- Ordered action checklist.
- “Not stated” or “Ambiguous—verify” fields instead of guessed values.
- A short plain-language summary.
- Evidence snippets or field-level source references where feasible.

This is a more direct match for an image-to-useful-result challenge than asking judges to wait for graph construction, persona generation, multi-agent simulation, and a long report.

## 3. Challenge requirements and fit

The challenge brief linked in the event repository is the source of the requirements below [1]. This assessment uses a five-point **internal readiness scale**, not an official judging score.

| Requirement from the challenge | Current code evidence | Preliminary readiness | Gap to close |
|---|---|---:|---|
| Meaningfully use Gemma 4 through the Gemini API | Current model layer is built around the Python OpenAI SDK and a compatible chat-completion wrapper. No Gemma 4 call was found in the reviewed snapshot. | 0/5 | Add and test a server-side Gemini API call using a supported Gemma 4 model ID. |
| Use multimodal input where it adds value | Current upload UI advertises PDF, Markdown, and TXT. Backend allowlist is PDF/MD/TXT. PNG/JPEG screenshot input is not supported by the current workflow. | 1/5 | Add image upload, validation, and image-to-Gemma request handling. |
| One clear user story | A general “predict the future” simulation workflow is broad. A campus notice-to-action flow is a clear, focused application. | 2/5 | Make the notice-to-action flow the primary path and postpone full simulation. |
| Working end-to-end prototype | The inherited project contains a multi-stage frontend/backend workflow, but this assessment did not execute it and cannot certify runtime success. | 3/5 | Validate setup and deliver one reliable, seeded end-to-end Gemma workflow. |
| Gemma-powered result obvious within 30 seconds | Current workflow involves several simulation stages and does not expose a Gemma-specific result. | 1/5 | Show the image and extracted action brief immediately in the demo story; minimize setup and loading friction. |
| Original contribution beyond the inherited project | The current snapshot mostly rebrands the upstream product. Campus-specific extraction, uncertainty handling, and an evaluation set are proposed but not implemented. | 1/5 | Implement and document original behavior, prompts, output schema, UI, and tests. |

**Overall preliminary readiness: approximately 1.3/5.** This is a source-based planning estimate, not an official score. The most important blockers are the missing Gemma 4 call, missing image-first path, and lack of a completed campus-specific feature.

## 4. What the uploaded repository currently contains

Static inspection of the uploaded ZIP found these components:

- **Frontend:** Vue 3, Vite, Vue Router, and Vue I18n.
- **Backend:** Python with Flask-style routes and services.
- **LLM abstraction:** `backend/app/utils/llm_client.py` uses the OpenAI Python SDK and an OpenAI-compatible completion helper. Configuration is controlled by `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL_NAME`.
- **Knowledge graph and memory:** Zep Cloud configuration and services, including `ZEP_API_KEY`.
- **Simulation:** Graph construction, ontology generation, simulated agent profiles, OASIS social simulation scripts, simulation management, and report generation.
- **Current upload formats:** PDF, Markdown, and TXT in the existing UI/backend configuration.
- **Existing license:** AGPL-3.0 file retained from the upstream project.

No `google-genai` dependency, `GEMINI_API_KEY` setting, or Gemma 4 implementation was found in the reviewed snapshot. The existence of a configurable model name does not by itself mean Gemma 4 is integrated: the current API wrapper and the model’s supported API behavior must be tested directly.

**Verification limit:** this was a source-code review only. The application was not installed, launched, or exercised with live credentials as part of this assessment.

## 5. Model and API approach

Google’s official Gemma 4 model card describes Gemma 4 as an open-weight model family with text and image input, and audio support on certain sizes [2]. Google’s Gemini API Gemma documentation currently lists the hosted models `gemma-4-31b-it` and `gemma-4-26b-a4b-it` [3]. Use a model ID explicitly supported by the documented API; do not substitute a Gemini-branded model such as `gemini-4-argon` and describe it as Gemma 4.

### Recommended implementation

1. Add the official Google Gen AI SDK (`google-genai`) to the backend dependencies, subject to the project’s dependency policy.
2. Add server-side configuration for `GEMINI_API_KEY` and a configurable Gemma model ID, defaulting to `gemma-4-26b-a4b-it` only after confirming it is enabled for the project’s API key and testing the actual request.
3. Implement a narrowly scoped endpoint, for example `POST /api/gemma/extract-notice`, rather than swapping every inherited LLM call at once.
4. Accept an image upload first (PNG/JPEG); validate file size and MIME type; reject unsupported or malformed inputs cleanly.
5. Send image plus a clear instruction to Gemma 4 through the Gemini API. Keep the key on the server; never put it in Vue code or browser-visible environment variables.
6. Parse the response into a typed, validated result object. Test structured-output or JSON-mode support for the chosen Gemma model; if that route is unsupported, request JSON in the prompt and apply strict server-side parsing and validation.
7. Render the result beside the original image, with missing/ambiguous fields visually explicit.

Do not rewire every existing stage of MiroFish to Gemma 4 during the first pass. That increases regression risk and makes it harder to prove precisely where Gemma adds value.

## 6. Recommended system architecture

**User uploads notice image → Flask validates file → Gemma 4 via Gemini API extracts information → schema validation and uncertainty checks → Vue renders action brief → optional later step launches scenario simulation.**

### Suggested result schema

```json
{
  "notice_title": "string or null",
  "notice_type": "event | policy | exam | scholarship | other | unknown",
  "event_date": "string or null",
  "registration_deadline": "string or null",
  "time": "string or null",
  "venue": "string or null",
  "eligibility": ["string"],
  "team_size": "string or null",
  "required_documents": ["string"],
  "registration_url": "string or null",
  "contact_details": ["string"],
  "action_items": [
    {
      "action": "string",
      "deadline": "string or null",
      "evidence": "short source excerpt or null"
    }
  ],
  "missing_or_ambiguous": ["string"],
  "plain_language_summary": "string",
  "verification_note": "AI-extracted details should be checked against the original notice"
}
```

Treat this as a proposed application schema, not a claim that it exists in the repository today. Dates, deadlines, URLs, and eligibility are high-risk extraction fields because plausible-looking errors can mislead users. Require the model to use `null` or an explicit “not stated” value when the source does not contain a fact. Do not infer a date from context unless the user explicitly asks for inference, and label inferred content separately.

### UI that judges should see

- Left side: the uploaded notice image.
- Right side: title, date/deadline, venue, eligibility, documents, and action checklist.
- A visually distinct “Missing or unclear in source” section.
- A visible label identifying the actual Gemma 4 model/API used.
- An error/retry state when the API fails, without losing the uploaded input.

Avoid fake confidence percentages unless you have calibrated and evaluated them. “Clearly stated,” “possibly ambiguous,” and “not found in source” are more defensible for the first prototype.

## 7. How to prove Gemma 4 is essential

The model must do more than power a generic chatbot. The demo should make its image-understanding contribution observable:

1. Upload a poster image containing mixed typography, compact text, dates, and a URL.
2. Show the original image and the extracted fields.
3. Demonstrate that the system identifies a deadline and eligibility rule that would be tedious to type manually.
4. Show an omitted or ambiguous detail being flagged rather than invented.
5. Convert the extracted details into a short, ordered action checklist.
6. Keep the Gemma 4 model ID in server logs and disclose it in the UI or submission technical notes.

A good demonstration is not merely “Gemma summarizes this.” It is “Gemma reads this visual campus notice, extracts source-grounded facts, and turns them into a usable student action plan while surfacing uncertainty.”

## 8. Build plan for a two-hour challenge

| Time | Milestone | Completion test |
|---|---|---|
| 0–10 min | Lock one user story and choose a known sample poster | The input and expected fields are written down before coding. |
| 10–25 min | Add the Gemini API configuration and one minimal Gemma request | A server-side request succeeds with the exact supported Gemma 4 model ID. |
| 25–45 min | Add PNG/JPEG upload and Flask endpoint | One uploaded image reaches the backend with validation. |
| 45–65 min | Add extraction prompt and response validation | API result becomes the proposed typed result object. |
| 65–80 min | Render action brief and ambiguity section | A user can compare extracted values with the original image. |
| 80–95 min | Test normal, incomplete, and unreadable notices | Missing fields are not invented; failures are handled cleanly. |
| 95–110 min | Polish one seeded demo and fallback result | Demo is repeatable even if live API access fails during judging. |
| 110–120 min | Rehearse short pitch and verify repository notes | Gemma contribution is visible quickly and the source link works. |

For a two-hour event, do not start by integrating the entire legacy simulation stack. If the event allows more development time, add scenario simulation after the focused Gemma workflow is stable.

## 9. Evaluation plan

Use a small, manually verified evaluation set before presenting accuracy claims. A practical first set is 12–20 public or synthetic campus notices with ground-truth labels. Include at least:

- A clear poster with all details present.
- A poster with a deadline in small text.
- A policy notice with eligibility requirements.
- A notice with no venue or registration link.
- A poster with conflicting dates or unclear typography.
- A low-quality screenshot.
- English and, if the selected model handles it reliably, Hindi or bilingual text.

Record at least these measures:

- **Critical-field accuracy:** event date, deadline, venue, eligibility, and registration URL.
- **Unsupported-claim rate:** number of returned factual claims not supported by the notice.
- **Missing-field honesty:** whether absent values are marked absent instead of guessed.
- **Action-list usefulness:** whether a human reviewer considers the required next steps complete and correctly ordered.
- **Latency and failure rate:** time from upload to result, plus request failures on repeat runs.

Do not advertise high accuracy based on one demonstration. Report results only after the evaluation set has actually been run and recorded.

## 10. Demonstration script

**Target length:** 60–90 seconds, with the core value obvious immediately.

1. “Campus notices often bury the deadline, eligibility, and required next step in a dense poster.”
2. Upload a prepared campus event poster.
3. Show Gemma 4 extracting the event title, date, deadline, eligibility, location, and requirements.
4. Point to one action checklist item and one “missing or unclear” item.
5. Explain that details not visible in the source are flagged rather than silently fabricated.
6. State the model ID and that the image is processed by Gemma 4 through the Gemini API.
7. Close with the outcome: students get an actionable summary without manually decoding the whole notice.

The seeded sample should be realistic, legally reusable, and tested twice. Keep a saved expected result or screenshot as a demo fallback, but clearly distinguish fallback data from a live model response.

## 11. Risks and mitigation

| Risk | Why it matters | Mitigation |
|---|---|---|
| Gemma 4 API is not integrated yet | Category requirement is currently unmet. | Build and test the focused endpoint first; do not rely on configurable model names alone. |
| Broad simulation scope | Multi-stage simulation can hide the value and take too long. | Treat notice extraction as the primary demo path; defer full simulation. |
| Hallucinated dates or requirements | Users could miss real deadlines or act on false instructions. | Preserve evidence snippets; use null/unknown values; add explicit verification note. |
| API quota, network, or key failure | A live demo may break. | Keep key server-side, add bounded retries/timeouts, and prepare a clearly labeled fallback. |
| Existing Zep dependency | Setup may fail before the new Gemma flow is demonstrated. | Isolate the focused extraction endpoint from Zep so its first end-to-end test does not depend on graph memory. |
| Branding could imply more is built than exists | The rename is currently ahead of the product implementation. | Keep the README and submission honest about planned versus completed functionality. |
| Upstream license obligations | The code is derived from AGPL-3.0 software. | Retain LICENSE and attribution, document modifications, and review network-service disclosure requirements. |
| Personal data in uploaded notices | Posters may include names, phone numbers, or private details. | Use public/synthetic demo inputs, avoid unnecessary retention, and state how uploads are handled. |

## 12. License, attribution, and submission integrity

This codebase is derived from **MiroFish** by 666ghj: https://github.com/666ghj/MiroFish. The original README is retained as `UPSTREAM_README.md`, the `LICENSE` file is preserved, and the project also credits OASIS for simulation infrastructure. The current license file is AGPL-3.0. Review the license and any dependency licenses before public deployment or submission.

Do not describe the project as independently built from scratch. For an honest submission, describe the inherited simulation foundation and identify the new original work precisely: the Gemma 4 endpoint, image-to-action extraction workflow, schema/uncertainty handling, UI, and the evaluation set—once those pieces actually exist.

## 13. Prioritized implementation checklist

### P0 — Required before a credible Gemma 4 demo
- [ ] Confirm the event API requirement with organizers if the challenge page has changed; the published brief specifies Gemini API.
- [ ] Obtain a working Gemini API key and verify access to the selected Gemma 4 model ID.
- [ ] Add a backend-only Gemma 4 service and minimal integration test.
- [ ] Support a PNG/JPEG notice upload.
- [ ] Return validated structured extraction and explicit missing/ambiguous fields.
- [ ] Render the result beside the source image.
- [ ] Label the actual Gemma model used and add a clear verification disclaimer.

### P1 — Needed to improve quality
- [ ] Add three or more difficult sample notices and compare results against manually prepared labels.
- [ ] Handle large, corrupt, unsupported, and low-quality images.
- [ ] Add latency logging, bounded retries, and readable error feedback.
- [ ] Add bilingual summary only after English extraction is reliable.
- [ ] Add tests for dates, links, null fields, and malformed model responses.

### P2 — Later extension, not a first-demo blocker
- [ ] Let a user run a campus policy scenario from the extracted notice.
- [ ] Reuse multi-agent simulation to compare possible stakeholder reactions.
- [ ] Add trend comparison, scenario history, and report generation.
- [ ] Explore offline/local Gemma deployment only if the event brief permits it and hardware/setup time allows.

## 14. Final assessment

**Decision: proceed, but re-scope before building.** CampusPulse AI has an inherited simulation base, yet that base is not the strongest first demonstration for the Best Use of Gemma 4 category. The winning path is not to replace every LLM call and run the full simulator. It is to prove one useful, multimodal, Gemma-powered workflow end to end, with source-grounded extraction, honest uncertainty handling, and a fast visual result.

Until the Gemma 4 API call, image upload, result UI, and tests exist and have been run, the project should be described as a **rebranded starter/fork with a proposed Gemma 4 plan**, not a completed Gemma 4 application.

## References

[1] MLH × DEV × React Hyderabad, “Best Use of Gemma 4” challenge brief, Hacktoberfest Hack Day 2026: https://github.com/reacthyderabad/hacktoberfest-hack-day-2026/blob/main/challenges/gemma-4.md

[2] Google AI for Developers, “Gemma 4 model card”: https://ai.google.dev/gemma/docs/core/model_card_4

[3] Google AI for Developers, “Run Gemma with the Gemini API”: https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api

[4] MiroFish upstream repository and preserved upstream README: https://github.com/666ghj/MiroFish

[5] GNU General Public License, version 3 (AGPL-3.0 text): https://www.gnu.org/licenses/agpl-3.0.html
