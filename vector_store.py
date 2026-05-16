import chromadb
from chromadb.utils import embedding_functions
import json
import os

DB_DIR = "chroma_db"

def init_db():
    client = chromadb.PersistentClient(path=DB_DIR)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.get_or_create_collection(
        name="resumes",
        embedding_function=sentence_transformer_ef
    )
    return collection

def index_resumes():
    collection = init_db()
    
    if collection.count() > 0:
        print("Resumes already indexed.")
        return

    resume_dir = "data/resumes"
    if not os.path.exists(resume_dir):
        print(f"Directory {resume_dir} not found. Run mock_data.py first.")
        return

    documents = []
    metadatas = []
    ids = []

    for filename in os.listdir(resume_dir):
        if filename.endswith(".json"):
            with open(os.path.join(resume_dir, filename), "r") as f:
                cand = json.load(f)
                doc_text = f"Name: {cand['name']}\nTitle: {cand['title']}\nExperience: {cand['experience']} years\nSkills: {', '.join(cand['skills'])}\nEducation: {cand['education']}\nSummary: {cand['summary']}"
                
                documents.append(doc_text)
                metadatas.append({"name": cand["name"], "title": cand["title"], "experience": cand["experience"]})
                ids.append(cand["id"])

    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully indexed {len(documents)} resumes.")

if __name__ == "__main__":
    index_resumes()
