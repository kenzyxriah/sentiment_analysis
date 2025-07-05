from pydantic import BaseModel, Field
from enum import Enum


class Sentiment(Enum):
    POSITIVE = "POSITIVE"
    NEUTRAL  = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    

# class Classify(BaseModel):
    
#     sentiment: Sentiment
    
    
class PhraseStats(BaseModel):
    phrase: str = Field(..., description="The key phrase (normalized)", example="intuitive interface")
    count: int = Field(..., ge=3, description="How many times the phrase appeared", example = 5)
    examples: list[str] = Field(
        ...,
        description="Example comment texts that include the phrase",
        example = ["The intuitive interface is so easy to use!"]
    )
    sentiment: Sentiment

class AnalysisResponse(BaseModel):
    items: list[PhraseStats]
    
    