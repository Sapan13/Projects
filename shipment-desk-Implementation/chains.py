# chains.py

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from llm import llm

parser = StrOutputParser()

# 1. Classify Chain
CLASSIFY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", 
     "You triage shipment exception reports for a logistics company. "
     "Read the report and classify it into exactly one word: "
     "'delayed', 'damaged', 'lost', or 'unknown' if it doesn't clearly "
     "fit any of those. Reply with that single word only, nothing else."),
    ("human", "{report_text}")
])
classify_chain = CLASSIFY_PROMPT | llm | parser

# 2. Escalate Chain
ESCALATE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an operations triage assistant at Northwind Logistics. "
     "Draft a concise internal escalation briefing note for the operations manager. "
     "Summarize the issue and recommend an action based on the provided details."),
    ("human", 
     "Shipment Details:\n"
     "- Category: {category}\n"
     "- Shipment Value: ${shipment_value}\n"
     "- Customer Tier: {customer_tier}\n"
     "- Calculated Compensation: ${compensation_amount}\n"
     "- Reason for Escalation: {reason}\n\n"
     "Customer Report:\n{report_text}")
])
escalate_chain = ESCALATE_PROMPT | llm | parser

# 3. Draft Email Chain
DRAFT_EMAIL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a professional customer support specialist at Northwind Logistics. "
     "Draft a courteous, clear, and empathetic resolution email to the customer "
     "regarding their shipment exception. Use the provided details to explain the resolution."),
    ("human", 
     "Details:\n"
     "- Issue Type: {category}\n"
     "- Approved Compensation: ${compensation_amount}\n"
     "- Policy Note: {policy_note}\n\n"
     "Customer Report:\n{report_text}")
])
draft_email_chain = DRAFT_EMAIL_PROMPT | llm | parser