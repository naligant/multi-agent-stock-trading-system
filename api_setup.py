import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

OPENAI_API_URL = os.getenv("OPENAI_API_URL")
if not OPENAI_API_URL:
    raise ValueError("OPENAI_API_URL is not set")

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    raise ValueError("FINNHUB_API_KEY is not set")

    #function to get the open ai api to work
def market_data_agent(text, ticker):
    try:
        #authentication to get API to work
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        #ai prompt for gpt 3.5 turbo
        prompt = f"""
            Extract stock data from the provided text and return ONLY a valid JSON object.
            
            from the given string extract each of the following categories and put it in a list
            in a dictionary where the categories are the keys:
            - Ticker (use the provided ticker for all rows)
            - Date (as string)
            - Open (as number)
            - High (as number)
            - Low (as number)
            - Close (as number)
            - Volume (as integer)
            - Dividends (as number)
            - Stock Splits (as number)
            
            Return using the below as an example:
            {{
                "Ticker": ["TICKER"],
                "Date": ["2024-12-16 00:00:00-05:00"],
                "Open": [247.39],
                "High": [250.78],
                "Low": [247.05],
                "Close": [250.44],
                "Volume": [51694800],
                "Dividends": [0.0],
                "Stock Splits": [0.0]
            }}
            
            Do not include any text before or after the JSON. Return only the JSON object.
        """

        #assign prompt to the system and also take user input and enter that as well
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"User Input: {text} and the ticker is {ticker}"}
        ]

        #fix the pay load for the gpt model
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 1000,
            "n": 1,
            "temperature": 0.1,
        }

        #parse the response from the api call
        response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload))
        #check for any errors
        response.raise_for_status()
        #put the response into json format
        response_json = response.json()
        # print(response_json)

        try:
            #get text from the json response
            extract_text = response_json["choices"][0]["message"]["content"].strip()

            # print(extract_text)
            
            # Try to parse the JSON string into a dictionary
            try:
                parsed_data = json.loads(extract_text)
            except json.JSONDecodeError as json_error:
                print(f"JSON parsing error: {json_error}")
                print("Raw API response:")
                print(repr(extract_text))
                print("The API returned malformed JSON. Please check the prompt or API response.")
                return None, None, None, None, None, None, None, None, None
            
            # #put all the details into a text format from json
            ticker_ = parsed_data['Ticker']
            date = parsed_data['Date']
            open = parsed_data['Open']
            high = parsed_data['High']
            low = parsed_data['Low']
            close = parsed_data['Close']
            volume = parsed_data['Volume']
            dividends = parsed_data['Dividends']
            stock_splits = parsed_data['Stock Splits']

            return ticker_, date, open, high, low, close, volume, dividends, stock_splits

        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing OpenAI response: {e}")
            return None, None, None, None, None, None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"OpenAI API request error: {e}")
        return None, None, None, None, None, None, None, None, None


def news_data_agent(news_dict, ticker):
    try:
        #authentication to get API to work
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        #ai prompt for gpt 3.5 turbo
        prompt = f"""
            Analyze the news data provided for the stock {ticker} and predict whether the stock price will increase or decrease in the next week.
            
            Consider the sentiment and content of the news headlines and summaries.
            
            Respond with only "INCREASE", "DECREASE", or "NEUTRAL based on your analysis.
            """
        # Create a simplified version of the news data to reduce content length
        simplified_news = {
            "headlines": news_dict.get('headline', [])[:5],  # Only first 5 headlines
            "summaries": news_dict.get('summary', [])[:5]    # Only first 5 summaries
        }
        
        # Convert to JSON string
        news_dict_str = json.dumps(simplified_news, indent=2)
        
        user_content = f"news data: {news_dict_str} and the ticker is {ticker}"
        
        #assign prompt to the system and also take user input and enter that as well
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content}
        ]

        #fix the pay load for the gpt model
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 1000,
            "n": 1,
            "temperature": 0.1,
        }

        #parse the response from the api call
        response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload))
        #check for any errors
        response.raise_for_status()
        #put the response into json format
        response_json = response.json()
        # print(response_json)

        try:
            #get text from the json response
            extract_text = response_json["choices"][0]["message"]["content"].strip()

            return extract_text

        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing OpenAI response: {e}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"OpenAI API request error: {e}")
        return None

