import streamlit as st

st.set_page_config(page_title="Smart Lost & Found Chatbot", page_icon="🔎")
st.title("🔎 Smart Lost & Found Chatbot")
st.caption("A simple rule-based prototype for reporting and finding misplaced items.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can help with lost and found items. Did you **lose** something or **find** something? Type `lost` or `found` to begin."}
    ]
if "reports" not in st.session_state:
    st.session_state.reports = [
        {"type": "found", "item": "black wallet", "colour": "black", "location": "college library"},
        {"type": "found", "item": "blue water bottle", "colour": "blue", "location": "canteen"},
        {"type": "lost", "item": "student ID card", "colour": "white", "location": "computer lab"},
    ]
if "stage" not in st.session_state:
    st.session_state.stage = "choice"
if "report" not in st.session_state:
    st.session_state.report = {}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def reply(text):
    st.session_state.messages.append({"role": "assistant", "content": text})

def handle(text):
    text = text.strip()
    low = text.lower()
    st.session_state.messages.append({"role": "user", "content": text})

    if st.session_state.stage == "choice":
        if "lost" in low:
            st.session_state.report = {"type": "lost"}
            st.session_state.stage = "item"
            reply("I'm sorry you lost it. What item are you looking for? (Example: black wallet)")
        elif "found" in low:
            st.session_state.report = {"type": "found"}
            st.session_state.stage = "item"
            reply("Thanks for helping! What item did you find?")
        else:
            reply("Please type **lost** or **found** so I know how to help.")
    elif st.session_state.stage == "item":
        st.session_state.report["item"] = text
        st.session_state.stage = "colour"
        reply("What colour is it? If the colour is unknown, type `unknown`.")
    elif st.session_state.stage == "colour":
        st.session_state.report["colour"] = text
        st.session_state.stage = "location"
        reply("Where did you last see it / where did you find it? Please enter a location.")
    elif st.session_state.stage == "location":
        st.session_state.report["location"] = text
        report = st.session_state.report
        if report["type"] == "lost":
            matches = [r for r in st.session_state.reports if r["type"] == "found" and
                       (report["item"].lower() in r["item"].lower() or r["item"].lower() in report["item"].lower()
                        or report["colour"].lower() == r["colour"].lower())]
            if matches:
                details = "\n".join([f"- **{m['item'].title()}** ({m['colour']}) — {m['location'].title()}" for m in matches])
                reply("I found possible matches in the sample records:\n\n" + details + "\n\nPlease contact your campus lost-and-found desk to verify ownership.")
            else:
                reply("I couldn't find a close match in the sample records. Your report has been noted in this session. Please check with the campus help desk.")
        else:
            st.session_state.reports.append(report.copy())
            reply(f"Thank you! Your **{report['item']}** report has been added to this session's sample records. Please hand the item to the campus lost-and-found desk.")
        st.session_state.stage = "choice"
        st.session_state.report = {}

if prompt := st.chat_input("Type your message..."):
    handle(prompt)
    st.rerun()

with st.sidebar:
    st.subheader("Prototype information")
    st.write("This demo uses Python rules and in-session sample data. It does not use an external LLM, database, RAG, or LangGraph.")
    if st.button("Restart conversation"):
        for key in ["messages", "stage", "report"]:
            st.session_state.pop(key, None)
        st.rerun()
    st.subheader("Sample records")
    for r in st.session_state.reports:
        st.write(f"• {r['item'].title()} — {r['location'].title()}")
