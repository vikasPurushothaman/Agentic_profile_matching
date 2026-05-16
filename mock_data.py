import os
import json

resumes = [
    {
        "id": "cand_001",
        "name": "Alice Smith",
        "title": "Senior Frontend Engineer",
        "experience": 5,
        "skills": ["React", "TypeScript", "Node.js", "Redux", "CSS", "Next.js"],
        "education": "BS Computer Science",
        "summary": "Experienced frontend engineer with a strong background in React and Next.js. Built scalable web applications for 5 years."
    },
    {
        "id": "cand_002",
        "name": "Bob Jones",
        "title": "Full Stack Developer",
        "experience": 3,
        "skills": ["Vue.js", "Python", "Django", "JavaScript", "PostgreSQL"],
        "education": "MS Software Engineering",
        "summary": "Full stack developer comfortable with Vue on the frontend and Python/Django on the backend."
    },
    {
        "id": "cand_003",
        "name": "Charlie Brown",
        "title": "Backend Engineer",
        "experience": 6,
        "skills": ["Java", "Spring Boot", "Microservices", "AWS", "SQL"],
        "education": "BS Computer Engineering",
        "summary": "Backend specialist focused on distributed systems and microservices architecture using Java and Spring."
    },
    {
        "id": "cand_004",
        "name": "Diana Prince",
        "title": "React Developer",
        "experience": 2,
        "skills": ["React", "JavaScript", "HTML", "CSS", "Tailwind"],
        "education": "Coding Bootcamp",
        "summary": "Passionate UI developer with 2 years of experience building responsive designs using React and Tailwind."
    },
    {
        "id": "cand_005",
        "name": "Evan Wright",
        "title": "Lead Software Engineer",
        "experience": 8,
        "skills": ["React", "Node.js", "AWS", "System Design", "TypeScript", "GraphQL"],
        "education": "BS Computer Science",
        "summary": "Lead engineer with 8 years of experience. Expert in full-stack JavaScript (React/Node) and cloud architecture."
    },
    {
        "id": "cand_006",
        "name": "Fiona Gallagher",
        "title": "Data Scientist",
        "experience": 4,
        "skills": ["Python", "Machine Learning", "Pandas", "SQL", "TensorFlow"],
        "education": "PhD Data Science",
        "summary": "Data scientist with expertise in predictive modeling and machine learning using Python."
    },
    {
        "id": "cand_007",
        "name": "George Miller",
        "title": "Frontend Developer",
        "experience": 4,
        "skills": ["Angular", "TypeScript", "RxJS", "SASS"],
        "education": "BS Information Technology",
        "summary": "Dedicated Angular developer with strong skills in TypeScript and reactive programming."
    },
    {
        "id": "cand_008",
        "name": "Hannah Abbott",
        "title": "DevOps Engineer",
        "experience": 5,
        "skills": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"],
        "education": "BS Computer Science",
        "summary": "DevOps engineer focusing on automation, containerization, and infrastructure as code."
    },
    {
        "id": "cand_009",
        "name": "Ian Malcolm",
        "title": "Senior React Native Engineer",
        "experience": 6,
        "skills": ["React Native", "React", "Mobile Development", "TypeScript", "Redux"],
        "education": "MS Computer Science",
        "summary": "Mobile developer with extensive experience building cross-platform apps using React Native."
    },
    {
        "id": "cand_010",
        "name": "Jane Doe",
        "title": "Junior Web Developer",
        "experience": 1,
        "skills": ["HTML", "CSS", "JavaScript", "React"],
        "education": "Self-Taught",
        "summary": "Enthusiastic junior developer eager to learn and grow in a fast-paced environment."
    }
]

def generate_mock_data():
    os.makedirs("data/resumes", exist_ok=True)
    for cand in resumes:
        with open(f"data/resumes/{cand['id']}.json", "w") as f:
            json.dump(cand, f, indent=4)
    print(f"Generated {len(resumes)} synthetic resumes in data/resumes/")

if __name__ == "__main__":
    generate_mock_data()
