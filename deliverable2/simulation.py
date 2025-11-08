# simulation.py — Robust utilities for Deliverable 2 (final)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any
import yaml

# --- Fallback personas so UI never crashes -----------------------------------
def _default_personas() -> Dict[str, Dict[str, Any]]:
    return {
        "product_manager": {
            "name": "Priya (PM)",
            "tone": "curious, outcome-focused, skeptical of scope creep",
            "goals": ["Validate user value", "Define success metrics", "Mitigate risks"],
        },
        "new_user": {
            "name": "Marco (New User)",
            "tone": "honest, novice perspective, sensitive to complexity",
            "goals": ["Understand basics quickly", "Avoid overwhelm", "Clear terminology"],
        },
        "accessibility_advocate": {
            "name": "Avery (A11y)",
            "tone": "principled, detail-oriented on inclusive design",
            "goals": ["Contrast, semantics, keyboard access, SR clarity", "Reduce cognitive load"],
        },
        "data_scientist": {
            "name": "Lisa (DS)",
            "tone": "methodical, metric-driven, skeptical of unproven claims",
            "goals": ["Define metrics", "Validate data quality", "Plan experimentation"],
        },
        "power_user": {
            "name": "Tessa (Power User)",
            "tone": "advanced, wants speed and control, dislikes hand-holding",
            "goals": ["Customization", "Keyboard efficiency", "Batch operations"],
        },
        "dpo": {
            "name": "Omar (DPO)",
            "tone": "risk-aware, compliance-driven",
            "goals": ["Minimize data sharing", "Ensure consent & transparency", "Govern retention"],
        },
    }

# --- Personas loader (dict or list supported) --------------------------------
def load_personas(path: str) -> Dict[str, Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return _default_personas()

    if isinstance(data, dict):
        return data

    if isinstance(data, list):
        out: Dict[str, Dict[str, Any]] = {}
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                continue
            key = item.get("key") or item.get("id") or item.get("name") or item.get("persona") or f"persona_{i+1}"
            out[str(key)] = item
        return out

    return _default_personas()

# --- OpenAI client w/ safe fallback ------------------------------------------
try:
    from openai import OpenAI, OpenAIError  # type: ignore
except Exception:
    OpenAI = None  # type: ignore
    class OpenAIError(Exception):  # type: ignore
        pass

# --- Conversation container ---------------------------------------------------
@dataclass
class Conversation:
    history: List[Dict[str, str]] = field(default_factory=list)
    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
    def to_messages(self) -> List[Dict[str, str]]:
        return list(self.history)

# --- Prompt builder -----------------------------------------------------------
def build_system_message(persona: Dict[str, Any]) -> Dict[str, str]:
    name = persona.get("name", "User Persona")
    tone = persona.get("tone", "neutral, concise")
    goals = persona.get("goals", [])
    goals_text = ", ".join(map(str, goals)) if goals else "Provide practical, concrete feedback."

    content = (
        "You are role-playing as a realistic product persona.\n"
        f"Persona name: {name}\n"
        f"Tone/style: {tone}\n"
        f"Primary goals: {goals_text}\n\n"
        "React to the feature description with honest observations, questions, risks, "
        "and suggestions, strictly from this persona's perspective."
    )
    return {"role": "system", "content": content}

# --- Engine: real API when available, MOCK otherwise --------------------------
class SimulationEngine:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        self.model = model
        self.temperature = temperature
        self.client = None
        if OpenAI is not None:
            try:
                self.client = OpenAI()  # uses env OPENAI_API_KEY
            except Exception:
                self.client = None

    def _mock_reply(self, messages: List[Dict[str, str]]) -> str:
        user_input = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
        return (
            "⚠️ MOCK RESPONSE (No API credits or client unavailable)\n"
            f"User said: {user_input}\n\n"
            "• Persona reaction: curious but skeptical about scope & UX clarity.\n"
            "• Potential issues: edge cases, privacy, performance, and rollout risk.\n"
            "• Suggestions: simplify the workflow, define success metrics, pilot with a small cohort.\n"
            "• Overall: promising if validated with real users; iterate quickly on feedback.\n"
        )

    def _chat(self, messages: List[Dict[str, str]]) -> str:
        if self.client is None:
            return self._mock_reply(messages)
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=350,
            )
            return resp.choices[0].message.content.strip()
        except OpenAIError:
            return self._mock_reply(messages)
        except Exception:
            return self._mock_reply(messages)

    def ask(self, system: Dict[str, str], persona: Dict[str, str],
            history: List[Dict[str, str]], prompt: str) -> str:
        messages = [system, persona] + history + [{"role": "user", "content": prompt}]
        return self._chat(messages)

# --- Synthesis (deterministic, API-free) -------------------------------------
def synthesize_feedback(conversations: Dict[str, Conversation]) -> str:
    lines: List[str] = ["### Persona Feedback Summary\n"]
    for key, convo in conversations.items():
        last_user = next((m.get("content", "") for m in reversed(convo.history) if m.get("role") == "user"), "")
        lines.append(
            f"**{key}**\n"
            f"- Reaction: constructive but cautious; wants clarity & measurable impact.\n"
            f"- Risks: complexity, edge cases, privacy/compliance, adoption friction.\n"
            f"- Suggestion: tighten scope, define success metrics, run a small pilot.\n"
            f"- Context (last user input): \"{last_user[:120]}...\"\n"
        )
    lines.append("\n**Overall Recommendation:** Pilot with 20–50 users, track leading metrics, iterate weekly.")
    return "\n".join(lines)

__all__ = [
    "load_personas",
    "Conversation",
    "SimulationEngine",
    "synthesize_feedback",
    "build_system_message",
]
