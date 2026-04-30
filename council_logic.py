import litellm
import os
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

class LLCouncil:
    def __init__(self):
        # Keys are now pulled directly from the environment
        self.chairman_model = "groq/llama-3.3-70b-versatile"

    def get_expert_opinions(self, question, models):
        responses = []
        for model in models:
            try:
                res = litellm.completion(model=model, messages=[{"role": "user", "content": question}])
                responses.append({
                    "model": model, 
                    "content": res.choices[0].message.content
                })
            except Exception as e:
                responses.append({"model": model, "content": f"Connection Error: {e}"})
        return responses

    def synthesize(self, question, drafts):
        # Format the experts' work for the Chairman
        context = "\n\n".join([f"--- DRAFT FROM {d['model']} ---\n{d['content']}" for d in drafts])
        
        prompt = f"""
        Analyze the following drafts for the question: "{question}"
        
        {context}
        
        Final Task: Provide a unified answer, note discrepancies, and check for hallucinations.
        """
        
        try:
            res = litellm.completion(model=self.chairman_model, messages=[{"role": "user", "content": prompt}])
            return res.choices[0].message.content
        except Exception as e:
            return f"The Chairman was unable to deliberate: {e}"