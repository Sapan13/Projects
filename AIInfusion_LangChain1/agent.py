# agent.py
# Block 11 — your first tiny AGENT: an LLM + one tool + a loop.
# The model decides, on its own, when to call the tool.
# Run:  python agent.py
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# ---- our tiny "database" (a dict standing in for a real one) ----
PRODUCTS = {"shoes": {"price": 799, "description": "Comfortable running shoes"},
          "hat": {"price": 399, "description": "Stylish baseball cap"}, 
          "bag": {"price": 1420, "description": "Durable backpack"}, 
          "shorts": {"price": 1299, "description": "Casual shorts"}, 
          "pants": {"price": 1699, "description": "Formal trousers"}}


# ---- Step 1: the tool is just a normal Python function ----
def get_price(item):
    print(f"🔧 tool called: get_price({item})")        # so you SEE it happen
    item_data = PRODUCTS.get(item.lower(), 'unknown')
    if item_data == 'unknown':
        return "Item not found."
    return f"₹{item_data['price']} "

def get_product_info(item):
    print(f"🔧 tool called: get_product_info({item})")        # so you SEE it happen
    item_data = PRODUCTS.get(item.lower(), 'unknown')
    if item_data == 'unknown':
        return "Item not found."
    return f"₹{item_data['price']} - {item_data['description']}"


# ---- Step 2: describe the tool so the model knows it exists ----
tools = [{
    "type": "function",
    "function": {
                "name": "get_price",
                "description": "Get the price of a shop item the user asks about.",
                "parameters": {
                                "type": "object",
                                "properties": {"item": {"type": "string", "description": "the item name"}},
                                "required": ["item"],
                            },
                },
        },
         {
    "type": "function",
    "function": {
                "name": "get_product_info",
                "description": "Get the product information including price and description.",
                "parameters": {
                                "type": "object",
                                "properties": {"item": {"type": "string", "description": "the item name"}},
                                "required": ["item"],
                            },
                },
        }
    ]


# ---- Step 3: the loop — think -> maybe call tool -> answer ----
def agent(user_message):
    messages = [{"role": "user", "content": user_message}]

    # 1. send the message + the tools menu; the model may ask for a tool
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools)
    msg = response.choices[0].message

    # 2. did it ask for a tool?
    if msg.tool_calls:
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)   # 3. read its request...
            if call.function.name == "get_price":
                result = get_price(args["item"])             #    ...and run the real function
            elif call.function.name == "get_product_info":
                result = get_product_info(args["item"]) 
            messages.append({
                "role": "tool",                          # a third role!
                "tool_call_id": call.id,
                "content": result,
            })
        # 4. send everything back so it can answer nicely
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        msg = response.choices[0].message

    return msg.content


if __name__ == "__main__":
    print(agent("How much are the shoes?"))       # -> uses the tool -> "₹799"
    print(agent("Hi! What can you help with?"))    # -> no tool needed -> just chats
