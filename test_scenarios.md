# Test Scenarios for Agentic Profile Matching

Here are 5 distinct conversation flows to test the capabilities of the LangGraph agent:

### Scenario 1: The Standard End-to-End Match
**Goal**: Verify the agent can take a standard JD, extract requirements, and rank candidates.
1. **User**: "We are looking for a Senior React Developer. Must have 5+ years of experience with React, TypeScript, and Next.js. Nice to have experience with Node.js and AWS."
2. **Expected Agent Behavior**:
   - Parses the input as a JD.
   - Extracts Must-Haves (React, TypeScript, Next.js, 5+ years) and Nice-to-Haves (Node.js, AWS).
   - Searches ChromaDB and shortlists top matches (e.g., Alice Smith, Evan Wright).
   - Generates a detailed report highlighting Alice's 5 years of React/Next.js experience.

### Scenario 2: Iterative Refinement
**Goal**: Verify the user can change requirements mid-conversation and see updated results.
1. **User**: (Following Scenario 1) "Actually, let's drop the Next.js requirement and focus on someone who has strong Python backend skills along with React."
2. **Expected Agent Behavior**:
   - The agent (via conversational loop) uses its tools or simply acknowledges the update. 
   - *Note: In a more advanced implementation, the agent would actively re-trigger the search node. Here, the user can just submit a new JD prompt to restart the pipeline, or the LLM can use the search tool directly to fetch new candidates.*

### Scenario 3: Head-to-Head Comparison
**Goal**: Verify the `compare_candidates` tool works.
1. **User**: "Compare cand_001 (Alice) and cand_005 (Evan) for a Lead Full Stack role."
2. **Expected Agent Behavior**:
   - The agent invokes the `compare_candidates` tool with `["cand_001", "cand_005"]`.
   - The agent returns a comparison summarizing that Evan has 8 years and more architectural/lead experience compared to Alice's 5 years.

### Scenario 4: Interview Question Generation
**Goal**: Verify the `generate_interview_questions` tool works.
1. **User**: "Generate interview questions for cand_006 (Fiona)."
2. **Expected Agent Behavior**:
   - The agent invokes `read_resume_file` or `generate_interview_questions` for `cand_006`.
   - The agent outputs 5 technical questions (about Python, TensorFlow, ML models) and 2 behavioral questions tailored to Fiona's data science background.

### Scenario 5: Vague Requirements & Clarification
**Goal**: Test how the agent handles broad or vague searches.
1. **User**: "Find me someone good with data."
2. **Expected Agent Behavior**:
   - Parses as a JD/Search Query.
   - Extracts "data" as a must-have.
   - Finds Fiona Gallagher (Data Scientist).
   - The user can follow up: "Do they know SQL?" -> Agent uses conversational context to confirm Fiona knows SQL based on her resume.
