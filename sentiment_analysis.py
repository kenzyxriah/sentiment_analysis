from sentiment_analysis.utils import fetch_comments
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pydantic import BaseModel, Field, model_validator
from fastapi import APIRouter, HTTPException
from typing import Any
router = APIRouter()



class Request(BaseModel):
    skip : int = Field(default = 0)
    take : int = Field(default = 100 ,ge= 0)
    subscriber_id : int = Field(gt=0)
    
    @model_validator(mode = 'after')
    def check_skip_take(self):
        if self.skip > self.take:
            raise ValueError(f"skip ({self.skip}) must not be greater than take ({self.take})")
        return self

from sentiment_analysis.src import SentimentAnalyzer

analyzer = SentimentAnalyzer()


class Response(BaseModel):
    percentages: dict[str, float]
    common_phrases: list[dict[str, Any]]


@router.post("/analyze_comments/", tags = ['Sentiment Analysis'], response_model= Response)
async def analyze_comments_endpoint(payload: Request):
    
    # Bad Request error
    if payload.take == 0: 
        logger.error("Invalid") 
        raise HTTPException(status_code=400, detail="take cannot be 0")

    # TODO: Get actual access token
    access_token = ''
    
    results : list[dict] = await fetch_comments(payload.skip, payload.take, payload.subscriber_id, access_token)
    logger.info("Fetched file data", extra={"data_size": len(results)})

    comments: list[str] = [i['comment'] for i in results if i['comment'] and i['comment'].strip()]
    
    if not comments:
        logger.error("No valid comments found")
        raise HTTPException(status_code=404, detail="No valid comments found")
    
    try:
        result = await analyzer.sentiment_analysis(comments)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
    


    
