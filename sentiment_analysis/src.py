from schemas import Sentiment, PhraseStats

from google import genai
from google.genai import types
from typing import Any

from dotenv import load_dotenv
load_dotenv()

import os


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)


class SentimentAnalyzer:
    
    def __init__(self):
        pass
    
    async def sentiment_analysis(self, comments: list[str]|str):
        
        if isinstance(comments, str):
            comments = [comments]
            
        try:
            analysis: list[str] = await self.analyze_comment_sentiment(comments)
            common_phrases = await self.analyze_phrases(comments)
            
            perc = {item: round(analysis.count(item) / len(analysis) * 100, 2) for item in set(analysis)}
            
            return {'percentages': perc, 'common_phrases': common_phrases}
            
        except genai.errors.APIError as e:
            raise e
        
        except json.JSONDecodeError as e:
            raise e
        
        except Exception as e:
            raise e     
    
    async def analyze_comment_sentiment(self, comments: list[str])-> list[str]:

            
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=comments, 
            config=types.GenerateContentConfig(
                system_instruction="""
            You are a sentiment classification assistant. 
            Classify each comment into one of the following labels: POSITIVE, NEUTRAL, or NEGATIVE.
            Return a JSON list of objects, one per input comment, each with a single key "sentiment" whose value is POSITIVE, NEUTRAL, or NEGATIVE.
            Do NOT return anything else.


                    Here are examples:
                    "I love this!" → POSITIVE  
                    "It was okay, nothing special." → NEUTRAL  
                    "I'm disappointed." → NEGATIVE

        """,
                response_mime_type="application/json",
                response_schema=list[Sentiment],
                temperature=0.0
            ),
        )
        return json.loads(response.text)


    async def analyze_phrases(self, comments: list[str], min_frequency= 3)-> list[dict[str, Any]]:
        """
        Extract common key phrases from comments using Gemini
        
        Args:
            comments (list): List of comment strings
            min_frequency (int): Minimum times a phrase must appear to be included
        
        Returns:
            list: List of dictionaries with phrase, count, and examples
        """
        
        
        prompt = """
        Analyze these comments and find common key phrases that appear multiple times.
        Focus on meaningful phrases or summarized sentiments (2-4 words) that represent features, complaints, or compliments.


        Return a JSON array [list] where each object has:
        - "phrase": the key phrase (normalized)
        - "count": how many times it appears across all comments
        - "examples": array of 3 or more original sentences containing this phrase
        - 'sentiment': 'POSITIVE', 'NEGATIVE', 'NEUTRAL'

        Only include phrases that appear at least min_frequency
        Focus on meaningful phrases like "intuitive interface", "slow performance", "customer service", "easy to use", etc.
        Ignore generic words like "good", "bad", "nice".

        Return only the JSON array, no other text.

        if there are no words that appear up to min_frequency, return an empty list

        """
        
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=comments,  
        config=types.GenerateContentConfig(
            system_instruction= f'{prompt}. Minimun Frequency is {min_frequency}', 
            response_mime_type="application/json",
            response_schema=list[PhraseStats],  
            temperature=0.0,
            ),
        )
        

        json_text = response.text.strip()
        
        
        phrases: list[dict] = json.loads(json_text)
        phrases.sort(key=lambda x: x['count'], reverse=True)
        
        return phrases
            

# if __name__ == "__main__":
#     # Sample comments for testing
#     import asyncio
    
#     sample_comments = [
#         "The interface is really intuitive and easy to use",
#         "Love the intuitive interface, makes everything simple",
#         "Performance is quite slow when loading large files",
#         "App crashes frequently, very frustrating",
#         "Customer service was helpful and responsive",
#         "The slow performance is really annoying",
#         "Great customer service team, solved my issue quickly",
#         "Interface design is intuitive but needs more features",
#         "Frequent crashes make this app unusable",
#         "Performance issues with slow loading times"
#     ]


#     analyzer = SentimentAnalyzer()
    
#     # Analyze phrases
#     print(asyncio.run(analyzer.sentiment_analysis(sample_comments)))
