import litellm
import os

# --- 1. SET YOUR KEYS ---
# LiteLLM looks for exactly these environment variable names
os.environ["GROQ_API_KEY"] = ""
os.environ["GEMINI_API_KEY"] = "" 

# --- 2. DEFINE THE TEST ---
question = "What are the most recent 2026 developments in solid-state battery density, and which company is leading the patent race?"

# --- 3. THE EXPERTS (STAGE 1) ---
# The "Elite" Google Council
models = [
    "gemini/gemini-2.5-pro",               # Expert 1: The "Thinking" Model
    "gemini/gemini-3.1-pro-preview",       # Expert 2: High Logic
    "gemini/gemma-3-27b-it"                # Expert 3: Diverse Perspective
]

responses = []
print("Council is deliberating...")

for i, model in enumerate(models):
    try:
        print(f"Asking Expert {i+1} ({model})...")
        res = litellm.completion(
            model=model, 
            messages=[{"role": "system", "content": "The current year is 2026. Provide your report based on the state of technology in 2026."}, {"role": "user", "content": question}]
        )
        responses.append(res.choices[0].message.content)
    except Exception as e:
        print(f"Expert {i+1} failed: {e}")
        responses.append("No response provided.")

print("\n" + "#"*20 + " RAW EXPERT DRAFTS " + "#"*20)
for idx, draft in enumerate(responses):
    print(f"\n--- [EXPERT {idx+1} FULL RESPONSE] ---")
    print(draft)
    print("-" * 50)


# --- 4. THE CHAIRMAN (STAGE 2) ---
# We keep Llama 3.3 as the Chairman for its excellent synthesis logic
chairman_prompt = f"""
You are the Chairman of the AI Council. 
A user asked: {question}

Below are 3 expert drafts. 
1. Synthesize them into one perfect, balanced answer.
2. If the experts disagree on a fact, highlight the disagreement and explain the consensus.
3. Explicitly point out any factual errors or "hallucinations."

Draft 1: {responses[0]}
Draft 2: {responses[1]}
Draft 3: {responses[2]}

Final Synthesis and Critique:
"""

print("\nChairman is synthesizing the final answer...")
try:
    final_answer = litellm.completion(
        model="groq/llama-3.3-70b-versatile", 
        messages=[{"role": "user", "content": chairman_prompt}]
    )
    print("\n" + "="*30 + " FINAL COUNCIL REPORT " + "="*30 + "\n")
    print(final_answer.choices[0].message.content)
except Exception as e:
    print(f"Chairman failed to synthesize: {e}")