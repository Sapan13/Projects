# 📦 Shipment Exception Desk

An AI-powered customer service triage pipeline designed to automate the processing of logistics exceptions (delays, damages, and lost items). Built with **LangChain** and **Gradio**, this application combines Large Language Models (LLMs) with deterministic business logic to classify issues, calculate compensation, and route tickets dynamically.

## 🚀 Key Features
* **Intelligent Classification:** Uses LangChain (LCEL) to parse natural language customer reports and strictly classify them into `delayed`, `damaged`, `lost`, or `unknown`.
* **Dynamic Business Rules:** Python functions calculate exact compensation percentages based on the severity of the issue (e.g., detecting keywords like "urgent" or "destroyed").
* **Tier-Based Routing:** 
  * **Standard Customers:** Tickets under $200 are auto-resolved.
  * **Premium Customers:** Tickets under $100 are auto-resolved (stricter escalation threshold for high-value clients).
* **Automated Drafting:** Generates empathetic customer emails for auto-resolutions or concise internal briefing notes for manager escalations.
* **Real-time Analytics:** Maintains a running daily log of total compensation, escalation rates, and the costliest exception category via the UI.

## 🛠️ Tech Stack
* **Python 3.x** 
* **LangChain** (LCEL, ChatPromptTemplates, StrOutputParser)
* **Gradio** (Web UI & State Management)
* **Groq API** (Ultra-fast LLM inference using the `ChatOpenAI` wrapper)

## 📂 Project Structure
* `app.py`: The Gradio web interface and frontend layout.
* `pipeline.py`: The core orchestration logic connecting the LLM chains to the business rules.
* `chains.py`: Contains the `ChatPromptTemplates` and LCEL chains utilizing strict `system` and `human` message roles.
* `tools.py`: Deterministic math and keyword-matching functions for calculating compensation.
* `session.py`: Handles state management and calculates the daily metrics summary.

## ⚙️ Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/raoul105/shipment-desk.git](https://github.com/raoul105/shipment-desk.git)
   cd shipment-desk
   ```

## 🛠️ Setup and Installation


2. Create a virtual environment (Recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Environment Variables:
   This project uses Groq's inference engine via the standard LangChain OpenAI wrapper.
   Create a .env file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   💻 Usage
   Start the Gradio application by running:
   ```
   python app.py
   ```
   The terminal will output a local URL (typically http://127.0.0.1:7860).
   Click it to open the interactive UI in your browser.



🧪 Example Scenarios
To test the system's routing logic and LLM classification, try the following inputs in the UI:

Test 1. Standard Auto-Resolution (Delay)

Customer Tier: Standard

Shipment Value: 50

Report: "My package arrived a day late, but it wasn't urgent."

Behaviour: Classifies as `delayed`, calculates $5.00 compensation (10%), 
stays under the $200 threshold, and drafts a customer email.

Test 2. Premium Escalation (Total Loss)

Customer Tier: Premium

Shipment Value: 500

Report: "My premium shipment was completely destroyed in transit."

Behaviour: Classifies as `damaged`, calculates $250.00 compensation (50% for "destroyed"), 
exceeds the $100 Premium threshold, and drafts a manager escalation note.

Test 3. Edge Case Handling/ Unknown Input

Customer Tier: Standard

Shipment Value: 10

Report: "fhjsdkfhkjsdhfjkdshf"

Behaviour: Safely classifies as `unknown`, calculates $0 compensation, automatically bypasses 
monetary thresholds, and escalates to a manager to prevent hallucinated compensation.
