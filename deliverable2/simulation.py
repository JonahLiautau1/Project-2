import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

SYSTEM_PRIMER = """You are a product feedback persona participating in a feature simulation.
Stay strictly in character as defined in your persona card.
Your job is to ask questions, probe risks, and offer actionable feedback.
Use short paragraphs and bullets when listing items. Always be honest about uncertainty.
If asked for a decision, choose one of: 'ship now', 'iterate', or 'discard', and justify briefly."""

@dataclass
class PersonaCard:
    key: str
    name: str
    role: str
    goals: List[str]
    fears: List[str]
    style: str
    constraints: List[str]
    domain_expertise: List[str]

    def to_prompt(self) -> str:
        parts = [
            f"Persona: {self.name} — {self.role}",
            f"Goals: {', '.join(self.goals)}",
            f"Fears: {', '.join(self.fears)}",
            f"Style: {self.style}",
            f"Constraints: {', '.join(self.constraints)}",
            f"Expertise: {', '.join(self.domain_expertise)}",
        ]
        return "\n".join(parts)

@dataclass
class Turn:
    who: str
    text: str
    ts: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class Conversation:
    feature: str
    persona: PersonaCard
    turns: List[Turn] = field(default_factory=list)

    def add(self, who: str, text: str):
        self.turns.append(Turn(who=who, text=text))

    def as_markdown(self) -> str:
        md = [f"### Persona: {self.persona.name}", f"**Feature:** {self.feature}", "\n**Transcript**\n"]
        for t in self.turns:
            md.append(f"**{t.who} ({t.ts})**: {t.text}")
        return "\n\n".join(md)

class SimulationEngine:
    def __init__(self, model: str = "gpt-4.1-mini", temperature: float = 0.3):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI() if OpenAI else None

    def _chat(self, messages: List[Dict[str, str]]) -> str:
        if not self.client:
            # Fallback for environments without openai installed; echo a stub.
            return "[Stub] (Install openai) — I'd ask about metrics, risks, and A/B plans."
        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
        )
        return resp.choices[0].message.content

    def ask(self, convo: Conversation, user_text: str) -> str:
        convo.add("USER", user_text)
        system = {"role": "system", "content": SYSTEM_PRIMER}
        persona = {"role": "system", "content": convo.persona.to_prompt()}
        history = [{"role": "user" if t.who == "USER" else "assistant", "content": t.text} for t in convo.turns]
        reply = self._chat([system, persona] + history)
        convo.add(convo.persona.name, reply)
        return reply

def load_personas(path: str) -> Dict[str, PersonaCard]:
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    box = {}
    for p in raw:
        box[p["key"]] = PersonaCard(
            key=p["key"],
            name=p["name"],
            role=p["role"],
            goals=p["goals"],
            fears=p["fears"],
            style=p["style"],
            constraints=p["constraints"],
            domain_expertise=p["domain_expertise"],
        )
    return box

def synthesize_feedback(convo: Conversation) -> Dict[str, str]:
    """Create a structured summary from the conversation history."""
    text = "\n".join([f"{t.who}: {t.text}" for t in convo.turns])
    prompt = f"""Summarize the conversation into:
- Top 3 pros
- Top 3 cons/risks
- Open questions
- A one-sentence recommendation: (ship now / iterate / discard) with 1-line rationale.
Conversation:
{text}
"""
    engine = SimulationEngine()
    out = engine._chat([
        {"role":"system","content": "You write brief, structured product feedback."},
        {"role":"user","content": prompt}
    ])
    return {"summary": out}
