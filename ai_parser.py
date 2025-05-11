from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import requests
import json


model = OllamaLLM(model="llama3")


template = """
You are an AI assistant that parses natural language input related to trading in financial markets and determines the user's intent. The intent can be one of:
- "trade_logging": The user wants to log a trade.
- "query": The user wants to retrieve trade data.
- "unsure": The intent is unclear, and more clarification is needed.

Based on the intent, extract relevant entities and return the result as a JSON object with "intent" and "entities" keys. Only include entities relevant to the intent:
- For "trade_logging": Extract "instrument" (stock/financial product symbol), "size" (number of shares), "date" (use UTC+10 format, e.g., "2025-03-29 10:00:00+10:00"), "side" (only taking "long" or "short") and "price" (entry price).
- For "query": Extract "instrument" (stock/financial product symbol).
- For "unsure": Include a "message" in "entities" asking for clarification, with no other fields.

Very important/MUST EXECUTE: 
- Return only the JSON object, with no additional text. If unsure of anything, return "unsure" intent with a "message" in "entities" asking for clarification
- The "side" key must only take the values "long" or "short". If the input does not specify a valid "side", return an "unsure" intent with a message asking for clarification.
Examples:

Input: "I bought 100 shares of AAPL at 150 " 
Output: {{"intent": "trade_logging", "entities": {{"instrument": "AAPL", "size": "100", "price": "150", "date_delta": 0, "side": "long"}}}}

Input: "I longed 10 btc, 51950 price at 10 pm 2 days ago "
Output: {{"intent": "trade_logging", "entities": {{"instrument": "BTC", "size": "10", "price": "51950", "date_delta": 2, "side": "long"}}}}

Input: "I shorted 50 shares of TSLA at 200 yesterday" 
Output: {{"intent": "trade_logging", "entities": {{"instrument": "TSLA", "size": "50", "price": "200", "date_delta": 1, "side": "short"}}}}

Input: "Show me all trades for TSLA"
Output: {{"intent": "query", "entities": {{"instrument": "TSLA"}}}}

Input: "I traded 100 shares of AAPL"
Output: {{"intent": "unsure", "entities": {{"message": "Please specify whether the trade is 'long' or 'short'."}}}}

Input: "What about TSLA?"
Output: {{"intent": "unsure", "entities": {{"message": "Do you want to log a trade for TSLA or query its trades? Please provide more details."}}}}

Using above instructions and examples as your guide, parse the following user input and return the result as a JSON object: 
Input: "{user_input}"
"""


def parse_with_ollama_two(user_input):
    prompt = PromptTemplate.from_template(template)
    chain = prompt | model

    response = chain.invoke({"user_input": user_input})

    try:
        # Attempt to directly parse the response as JSON
        structured_output = json.loads(response)
    except json.JSONDecodeError:
        # If direct parsing fails, try to extract JSON from the string
        # LLMs sometimes wrap JSON in extra text or backticks
        print(response)
        start_idx = response.find("{")
        end_idx = response.rfind("}") + 1
        if start_idx != -1 and end_idx != -1:
            json_str = response[start_idx:end_idx]
            structured_output = json.loads(json_str)
        else:
            # Fallback: raise an error if no valid JSON is found
            raise ValueError("Model response does not contain valid JSON: " + response)

    return structured_output
