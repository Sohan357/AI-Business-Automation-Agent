from langchain_ollama import ChatOllama
from data import crm_leads, candidates, projects

llm = ChatOllama(
    model="llama3",
    temperature=0
)

audit_logs = []


def add_audit(role, action):
    audit_logs.append({
        "role": role,
        "action": action
    })


def search_lead(query):
    results = []

    for lead in crm_leads:
        if query.lower() in lead["name"].lower():
            results.append(lead)

    return results


def high_priority_leads():
    return [
        lead
        for lead in crm_leads
        if lead["score"] > 80
    ]


def generate_email(name, project):

    lead = next(
        (lead for lead in crm_leads
         if lead["name"].lower() == name.lower()),
        None
    )

    if not lead:
        return "Lead not found."

    prompt = f"""
Generate a professional sales follow-up email.

Lead Name: {lead['name']}
Company: {lead['company']}
Project: {project}

Sender Name: AI Business Automation Team
Sender Role: Sales Manager

Rules:
- Use the lead name.
- Use the company name.
- Use the project name.
- Do NOT use placeholders such as:
  [Your Name]
  [Company]
  [Product]
  [Service]
- Do NOT ask the user to fill anything in.
- Write the complete email.
- End with exactly:

Best Regards,
AI Business Automation Team
Sales Manager
"""

    response = llm.invoke(prompt)

    return response.content
def screen_candidate(name):
    for candidate in candidates:

        if name.lower() in candidate["name"].lower():

            score = min(
                100,
                candidate["experience"] * 15 +
                len(candidate["skills"]) * 10
            )

            return {
                "candidate": candidate,
                "score": score
            }

    return "Candidate not found"


def project_risks():

    return [
        p for p in projects
        if p["status"] == "Delayed"
    ]


def business_summary():

    prompt = f"""
Generate a business summary.

CRM:
{crm_leads}

Candidates:
{candidates}

Projects:
{projects}
"""

    return llm.invoke(prompt).content