import os, time
from dotenv import load_dotenv
from tinytroupe.examples import create_lisa_the_data_scientist

load_dotenv()

def run_once(feature: str):
    lisa = create_lisa_the_data_scientist()
    transcript = []

    def step(msg):
        transcript.append(("USER", msg))
        reply = lisa.listen_and_act(msg)
        transcript.append(("LISA", str(reply)))

    step(f"You are evaluating a proposed feature: {feature}. What are your initial thoughts?")
    step("List top 3 pros and top 3 cons.")
    step("Give a one-sentence recommendation (ship now / iterate / discard).")
    return transcript

def save_transcript(transcript, feature, path="conversations/D1_conversations.md"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n\n## Run — {ts}\n")
        f.write(f"**Persona:** Lisa the Data Scientist\n")
        f.write(f"**Feature:** {feature}\n\n")
        f.write("**Transcript**\n\n```\n")
        for who, text in transcript:
            f.write(f"{who}: {text}\n\n")
        f.write("```\n\n")
        f.write("**Comments on conversation quality**\n")
        f.write("- Coherence:\n- Persona consistency:\n- Usefulness:\n- Limitations:\n")

if __name__ == "__main__":
    feature = input("Feature to evaluate (e.g., 'Dark Mode in mobile app'): ").strip()
    convo = run_once(feature)
    for who, text in convo:
        print(f"{who}: {text}\n")
    save_transcript(convo, feature)
    print("\nSaved to conversations/D1_conversations.md")
