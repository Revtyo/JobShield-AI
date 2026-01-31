import re
from sentence_transformers import SentenceTransformer, util
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from rake_nltk import Rake

# Initialize models
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
gpt_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt_model = GPT2LMHeadModel.from_pretrained('gpt2')

# analyzer.py refinement
def get_universal_keywords(resume_text, job_desc):
    r = Rake(min_length=1, max_length=3)
    r.extract_keywords_from_text(job_desc)
    
    # Filter list for common "UI Noise"
    noise = {"ago", "days", "policy", "cookie", "apply", "sign", "agreement", "posted", "hiring"}
    
    raw_phrases = r.get_ranked_phrases()
    clean_phrases = [p for p in raw_phrases if not any(w in p.lower() for w in noise)]
    
    # Return top 8 missing phrases as a clean bulleted list
    return [p for p in clean_phrases[:8] if p.lower() not in resume_text.lower()]

def check_ats_compliance(resume_text):
    """Scans for structural issues that cause ATS parsing failures."""
    flags = []
    
    # 1. Check for Contact Info
    if not re.search(r'[\w\.-]+@[\w\.-]+', resume_text):
        flags.append("Missing Email Address")
    if not re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text):
        flags.append("Missing or non-standard Phone Number")

    # 2. Check for Standard Section Headers
    headers = ["Experience", "Education", "Skills", "Projects", "Summary"]
    found_headers = [h for h in headers if h.lower() in resume_text.lower()]
    if len(found_headers) < 3:
        flags.append("Missing standard section headers (Experience, Education, etc.)")

    # 3. Structural Red Flags
    if " | " in resume_text and len(resume_text.split(" | ")) > 5:
        flags.append("Possible complex column/table layout detected")

    status = "Pass" if not flags else "Needs Improvement"
    return {"status": status, "flags": flags}

def get_application_strength(resume, job_desc):
    """Uses Semantic Similarity (Sentence-BERT) to judge match strength."""
    emb1 = embed_model.encode(resume)
    emb2 = embed_model.encode(job_desc)
    score = util.cos_sim(emb1, emb2).item()
    return round(score * 100, 2)

def check_ai_genericity(text):
    """Calculates perplexity; lower scores indicate predictable AI-like text."""
    inputs = gpt_tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        outputs = gpt_model(**inputs, labels=inputs["input_ids"])
    perplexity = torch.exp(outputs.loss).item()
    status = "Human-Like" if perplexity > 40 else "Too Generic/AI"
    return {"status": status, "score": round(perplexity, 2)}