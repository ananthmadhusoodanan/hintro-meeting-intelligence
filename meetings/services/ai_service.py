import json
import os
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def analyze_transcript(transcript: list, participants: list) -> dict:
    transcript_text = "\n".join([
        f"[{seg['timestamp']}] {seg['speaker']}: {seg['text']}"
        for seg in transcript
    ])
    participants_text = ", ".join(participants)

    prompt = f"""You are a meeting intelligence assistant. Analyze the following meeting transcript and extract structured insights.

PARTICIPANTS: {participants_text}

TRANSCRIPT:
{transcript_text}

STRICT RULES:
1. Only use information explicitly present in the transcript
2. Do not invent attendees, action items, decisions, or outcomes
3. Every insight MUST include a citation with the exact timestamp from the transcript
4. If something is unclear or not mentioned, do not include it

Return ONLY valid JSON in this exact format, nothing else:
{{
  "summary": [
    {{
      "text": "brief summary point",
      "citations": [{{"timestamp": "MM:SS"}}]
    }}
  ],
  "actionItems": [
    {{
      "task": "what needs to be done",
      "assignee": "person responsible (email if known, else name)",
      "dueDate": null,
      "citations": [{{"timestamp": "MM:SS"}}]
    }}
  ],
  "decisions": [
    {{
      "text": "decision that was made",
      "citations": [{{"timestamp": "MM:SS"}}]
    }}
  ],
  "followUpSuggestions": [
    {{
      "text": "suggested follow-up action",
      "citations": [{{"timestamp": "MM:SS"}}]
    }}
  ]
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1024
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)
