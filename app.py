import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

load_dotenv() 

from matching_agent import app as agent_app

st.set_page_config(page_title="Agentic Profile Matching", layout="wide")
st.title("🤝 Agentic Profile Matching System")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "state" not in st.session_state:
    st.session_state.state = {"messages": []}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat Interface")

    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            if msg.content:
                with st.chat_message("assistant"):
                    st.write(msg.content)
        elif isinstance(msg, ToolMessage):
            with st.chat_message("tool"):
                st.write(f"🔧 Tool Result: {msg.name}")

    if prompt := st.chat_input("Enter a Job Description or ask a question about candidates..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("Agent is thinking..."):
            current_state = st.session_state.state
            current_state["messages"] = st.session_state.messages
            new_state = agent_app.invoke(current_state)
            st.session_state.state = new_state
            st.session_state.messages = new_state["messages"]
            st.rerun()

with col2:
    st.subheader("Current State")

    state = st.session_state.state

    if "requirements" in state and state["requirements"]:
        with st.expander("📝 Extracted Requirements", expanded=True):
            reqs = state["requirements"]
            st.markdown("**Must Have:**")
            for req in reqs.get("must_have", []):
                st.markdown(f"- {req}")
            st.markdown("**Nice to Have:**")
            for req in reqs.get("nice_to_have", []):
                st.markdown(f"- {req}")

    if "shortlist" in state and state["shortlist"]:
        with st.expander("🏆 Candidate Shortlist", expanded=True):
            for i, cand in enumerate(state["shortlist"]):
                st.markdown(f"**{i+1}. {cand.get('metadata', {}).get('name', 'Unknown')}**")
                st.markdown(f"*{cand.get('metadata', {}).get('title', '')}*")
                st.caption(f"ID: {cand.get('id', '')}")
                st.divider()

    if "reports" in state and state["reports"]:
        with st.expander("📊 Latest Report", expanded=True):
            st.markdown(state["reports"].get("latest", "No report generated yet."))

    # ── API Key Status ───────────────────────────────────────────────────────
    st.subheader("⚙️ Configuration")
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and not api_key.startswith("sk-your-"):
        st.success("✅ OpenAI API key loaded from .env", icon="🔑")
    else:
        st.error("❌ No API key found. Add `OPENAI_API_KEY=sk-...` to the `.env` file.", icon="🔑")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    st.caption(f"Model: `{model}`")

    st.divider()

    # ── Data Setup ───────────────────────────────────────────────────────────
    st.subheader("🗄️ Data Setup")
    if st.button("Generate Mock Resumes & Index DB"):
        with st.spinner("Generating mock data..."):
            os.system("python mock_data.py")
            os.system("python vector_store.py")
            st.success("Mock data generated and indexed into ChromaDB!")
