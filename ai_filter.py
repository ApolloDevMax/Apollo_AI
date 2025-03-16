import openai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

# Function to analyze an earning method


def analyze_earning_method(description):
    prompt = f"""
    You are an expert in making money online. Evaluate this method and determine if it can realistically generate $100 quickly.
    
    Description: {description}
    
    Rate it on three criteria (0-10):
    1. Profitability
    2. Speed of payout
    3. Difficulty level
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content


# Example usage
method = "Writing articles on TextBroker"
analysis = analyze_earning_method(method)
print(analysis)
