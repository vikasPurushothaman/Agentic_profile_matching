import json
from typing import Literal
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from state import AgentState
from llm_config import get_llm
from tools import (
    search_resumes_rag,
    read_resume_file,
    extract_requirements,
    compare_candidates,
    generate_interview_questions
)

_llm = None
_llm_with_tools = None

def _get_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm

def _get_llm_with_tools():
    global _llm_with_tools
    if _llm_with_tools is None:
        tools = [
            search_resumes_rag,
            read_resume_file,
            extract_requirements,
            compare_candidates,
            generate_interview_questions
        ]
        _llm_with_tools = _get_llm().bind_tools(tools)
    return _llm_with_tools

# Bind tools for the human feedback / conversational node
tools = [
    search_resumes_rag,
    read_resume_file,
    extract_requirements,
    compare_candidates,
    generate_interview_questions
]

def parse_jd(state: AgentState):
    """Parses the latest user message to see if it's a new job description or a general query."""
    messages = state.get("messages", [])
    if not messages:
        return {"job_description": ""}
        
    last_message = messages[-1].content
    
    prompt = f"Is the following text a Job Description (JD) / list of requirements, or is it a conversational question? Respond with exactly 'JD' or 'QUESTION'.\n\nText: {last_message}"
    intent = _get_llm().invoke(prompt).content.strip()
    
    if intent == "JD" or len(last_message) > 100:
        return {"job_description": last_message}
    return {}

def extract_reqs(state: AgentState):
    """Extract requirements from the JD."""
    jd = state.get("job_description", "")
    if jd:
        reqs_json = extract_requirements.invoke({"jd": jd})
        try:
            reqs = json.loads(reqs_json)
            return {"requirements": reqs}
        except:
            return {"requirements": {"must_have": [], "nice_to_have": []}}
    return {}

def search_resumes(state: AgentState):
    """Search for candidates based on requirements."""
    reqs = state.get("requirements", {})
    if not reqs.get("must_have"):
        return {}
        
    query = " ".join(reqs.get("must_have", [])) + " " + " ".join(reqs.get("nice_to_have", []))
    results_json = search_resumes_rag.invoke({"query": query, "n_results": 10})
    try:
        candidates = json.loads(results_json)
        return {"shortlist": candidates}
    except:
        return {"shortlist": []}

def rank_candidates(state: AgentState):
    """Rank the shortlisted candidates using the LLM."""
    shortlist = state.get("shortlist", [])
    reqs = state.get("requirements", {})
    
    if not shortlist:
        return {}
        
    prompt = f"Rank these candidates based on the following requirements:\nRequirements: {json.dumps(reqs)}\nCandidates: {json.dumps(shortlist)}\nReturn the ranked list of candidate IDs in order of best match to worst match. Format as a JSON array of strings."
    
    try:
        ranking_response = _get_llm().invoke(prompt).content
        start = ranking_response.find("[")
        end = ranking_response.rfind("]") + 1
        ranked_ids = json.loads(ranking_response[start:end])
        
        ranked_shortlist = sorted(shortlist, key=lambda x: ranked_ids.index(x["id"]) if x["id"] in ranked_ids else 999)
        return {"shortlist": ranked_shortlist}
    except Exception as e:
        print("Error ranking:", e)
        return {}

def generate_report(state: AgentState):
    """Generate explainability report for top candidates."""
    shortlist = state.get("shortlist", [])
    reqs = state.get("requirements", {})
    
    if not shortlist:
        return {}
        
    top_candidates = shortlist[:3] 
    prompt = f"Generate a detailed match report highlighting strengths, gaps, and improvement suggestions for these top candidates against the requirements.\nRequirements: {json.dumps(reqs)}\nCandidates: {json.dumps(top_candidates)}"
    
    report = _get_llm().invoke(prompt).content
    
    reports = state.get("reports", {})
    reports["latest"] = report
    
    return {"reports": reports, "messages": [AIMessage(content=report)]}

def human_feedback(state: AgentState):
    """Handles conversation, tool calls, and human feedback."""
    messages = state["messages"]
    
    if isinstance(messages[-1], AIMessage) and not messages[-1].tool_calls:
        return {}
        
    response = _get_llm_with_tools().invoke(messages)
    return {"messages": [response]}

def route_after_parse(state: AgentState) -> Literal["extract_reqs", "human_feedback"]:
    if state.get("job_description") and state["messages"][-1].content == state.get("job_description"):
        return "extract_reqs"
    return "human_feedback"

def route_after_tools(state: AgentState) -> Literal["human_feedback", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "execute_tools"
    return "__end__"

from langgraph.prebuilt import ToolNode
tool_node = ToolNode(tools)

workflow = StateGraph(AgentState)

workflow.add_node("parse_jd", parse_jd)
workflow.add_node("extract_reqs", extract_reqs)
workflow.add_node("search_resumes", search_resumes)
workflow.add_node("rank_candidates", rank_candidates)
workflow.add_node("generate_report", generate_report)
workflow.add_node("human_feedback", human_feedback)
workflow.add_node("execute_tools", tool_node)

workflow.add_edge(START, "parse_jd")
workflow.add_conditional_edges("parse_jd", route_after_parse)

# Main pipeline flow
workflow.add_edge("extract_reqs", "search_resumes")
workflow.add_edge("search_resumes", "rank_candidates")
workflow.add_edge("rank_candidates", "generate_report")
workflow.add_edge("generate_report", END)

# Conversational flow
workflow.add_conditional_edges("human_feedback", route_after_tools)
workflow.add_edge("execute_tools", "human_feedback")

# Compile
app = workflow.compile()
