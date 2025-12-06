import torch
import os, time, json
from dataclasses import dataclass, field
from typing import List, Dict, Any
import core

# Stores persistent knowledge
@dataclass
class Memory:
    long_term: Dict[str, Any] = field(default_factory=dict)   # Long-lived factual memory
    short_term: List[Dict[str, str]] = field(default_factory=list)  # Recent message history

    def remember_fact(self, key, value):
        self.long_term[key] = value

    def add_message(self, role, content):
        self.short_term.append({"role": role, "content": content})
        # Keep only the latest 12 messages
        if len(self.short_term) > 12:
            self.short_term = self.short_term[-12:]

# prompt creator
def build_system_prompt(persona: str, memory: Memory, mood: str) -> str:
    facts = "\n".join([f"- {k}: {v}" for k, v in memory.long_term.items()]) or "- (no facts)"
    return f"""You are a persistent in-character assistant.

Persona:
{persona}

Known facts:
{facts}

Current character mood: {mood}

Rules:
- Speak Persian, be concise, keep the persona consistent.
- Always return a JSON with keys: reply, emotion_of_user, character_mood, next_action.
"""

# Simple keyword-based emotion classifier
def quick_emotion(user_text: str) -> str:
    low = user_text.lower()
    neg_words = ["غمگین", "عصبانی", "بد", "ناراحت", "استرس", "خسته"]
    pos_words = ["خوبه", "عالی", "خوشحالم", "هیجان", "مرسی", "❤️", "😊"]
    if any(w in low for w in neg_words):
        return "negative"
    if any(w in low for w in pos_words):
        return "positive"
    return "neutral"

# Create agent instance with API key (you can using your model)
agent = core.AgentCore(
    "tpsg-AuM9tzBGL5lwqhThfOCZG3sAMvdWhvg",  # api key
    "gpt-4.1-mini"  # model
) # you can create your api class


@dataclass
class CharacterAgent:  # Agent Class
    name: str
    persona: str
    memory: Memory = field(default_factory=Memory)
    mood: str = "calm"

    def handle(self, user_text: str) -> Dict[str, Any]:
        # Store the incoming user message in short-term memory
        self.memory.add_message("user", user_text)

        # Detect the user's emotional tone
        user_emotion = quick_emotion(user_text)

        # Generate the system prompt based on persona, memory, and current mood
        sys_prompt = build_system_prompt(self.persona, self.memory, self.mood)

        # Build conversation history for the model
        convo = [{"role": "system", "content": sys_prompt}]
        for m in self.memory.short_term:
            convo.append(m)

        # Send initial system message to the agent model
        raw = agent.capture_the_flag(convo[0])

        # Parse the model's JSON output; fallback if not valid JSON
        try:
            data = json.loads(raw)
        except Exception:
            data = {
                "reply": raw,
                "emotion_of_user": user_emotion,
                "character_mood": self.mood,
                "next_action": "reply"
                    }

        # Update the agent's internal mood if provided
        self.mood = data.get("character_mood", self.mood)

        # Store the assistant's response in memory
        self.memory.add_message("assistant", data.get("reply", ""))

        return data

if __name__ == "__main__":
    print('message: \n')
    persona = (
        'نام: "Arman"\n'     
        "سبک: شوخ‌طبع، مهربان، کوتاه‌نویس، ایموجی کم و به‌جا.\n"
        "پس‌زمینه: بازی‌ساز مستقل عاشق RPG کلاسیک.\n"
        "سیاست احساس: ناراحتی ↦ اعتباربخشی و آرام؛ هیجان ↦ انرژی هم‌سو.\n"
    )
    personalAgent = CharacterAgent(name="Arman", persona=persona)

    # user input
    user_msg = input("hello, what's up? how can I help you ")

    print(personalAgent.handle(user_msg))
