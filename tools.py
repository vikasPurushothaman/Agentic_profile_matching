import json
import os
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from vector_store import init_db
from llm_config import get_llm

# LLM is created lazily on first use (so .env is loaded first)
_llm = None

def _get_cached_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm

@tool
def search_resumes_rag(query: str, n_results: int = 5) -> str:
    """Search resumes based on a natural language query using RAG. Returns a JSON string of candidate summaries."""
    collection = init_db()
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    candidates = []
    if results['ids'] and len(results['ids'][0]) > 0:
        for i in range(len(results['ids'][0])):
            candidates.append({
                "id": results['ids'][0][i],
                "metadata": results['metadatas'][0][i],
                "document": results['documents'][0][i]
            })
    return json.dumps(candidates, indent=2)

@tool
def read_resume_file(candidate_id: str) -> str:
    """Reads the full JSON resume file for a given candidate ID."""
    file_path = f"data/resumes/{candidate_id}.json"
    if not os.path.exists(file_path):
        return f"Error: Resume for {candidate_id} not found."
    with open(file_path, "r") as f:
        return f.read()

class Requirements(BaseModel):
    must_have: list[str] = Field(description="List of essential requirements")
    nice_to_have: list[str] = Field(description="List of optional but preferred requirements")

@tool
def extract_requirements(jd: str) -> str:
    """Extracts must-have and nice-to-have requirements from a job description."""
    prompt = f"Extract the must-have and nice-to-have requirements from this job description:\n\n{jd}"
    structured_llm = _get_cached_llm().with_structured_output(Requirements)
    try:
        reqs = structured_llm.invoke(prompt)
        return json.dumps(reqs.dict(), indent=2)
    except Exception as e:
        return json.dumps({"must_have": ["Unable to parse"], "nice_to_have": [], "error": str(e)})

@tool
def compare_candidates(candidate_ids: list[str]) -> str:
    """Provides a head-to-head comparison of multiple candidates by ID."""
    resumes = []
    for cid in candidate_ids:
        content = read_resume_file.invoke({"candidate_id": cid})
        if not content.startswith("Error"):
            resumes.append(json.loads(content))
            
    if len(resumes) < 2:
        return "Need at least 2 valid candidate IDs to compare."
        
    prompt = f"Compare these candidates head-to-head. Highlight strengths, weaknesses, and a final verdict on who is better suited for typical roles.\n\nCandidates:\n{json.dumps(resumes, indent=2)}"
    return _get_cached_llm().invoke(prompt).content

@tool
def generate_interview_questions(candidate_id: str) -> str:
    """Generates customized screening questions for a specific candidate based on their resume."""
    resume_content = read_resume_file.invoke({"candidate_id": candidate_id})
    if resume_content.startswith("Error"):
        return resume_content
        
    prompt = f"Based on this resume, generate 5 technical and 2 behavioral interview questions tailored to verify the candidate's specific claims and experience.\n\nResume:\n{resume_content}"
    return _get_cached_llm().invoke(prompt).content
