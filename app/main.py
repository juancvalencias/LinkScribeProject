import joblib
import pandas as pd
import requests
import base64

from pymongo import MongoClient
from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel
from backend.tools import ScrapTool, TextClassifier
from backend.database import MongoDBHandler
from typing import Optional, List


app: FastAPI = FastAPI()
mongo_handler = MongoDBHandler()
scraper = ScrapTool()
text_classifier = None

model_path = "./backend/data/web_classifier.joblib"  
vectorizer_path = "./backend/data/tfidf_vectorizer.joblib"  
id_to_category = {0:"Travel", 1:"Social Networking and Messaging", 2:"News", 
                          3: "Streaming Services",4: "Sports", 5:"Photographys", 6:"Law and Government", 
                          7:"Health and Fitness" , 8:"Games", 9:"E-Commerce", 10:"Forums",
                          11:"Food", 12:"Education", 13:"Computers and Technology", 14:"Business/Corporate", 
                          15:"Adult"}

class SearchRequest(BaseModel):
    url: str

class SaveRequest(BaseModel):
    url: str
    category: str
    summary: str

class Item(BaseModel):
    url: str

class Result(BaseModel):
    category: Optional[str] = None
    summary: Optional[str] = None
    image_base64: Optional[str] = None
    error: Optional[str] = None

class SearchResults(BaseModel):
    results: List[SaveRequest]

class SavedLink(BaseModel):
    url: str
    category: Optional[str] = None
    summary: Optional[str] = None

async def lifespan(app: FastAPI):
    global text_classifier
    try:       
        
        text_classifier = TextClassifier(model_path, vectorizer_path, id_to_category)
        yield
    finally:
        
        mongo_handler.close_connection()
        print("MongoDB connection closed on shutdown.")

app = FastAPI(lifespan=lifespan)


@app.post("/save")
async def save_search_data(request: SaveRequest):
    print(request.model_dump())
    mongo_handler.store_search_data(request.url, request.category, request.summary)
    return {"message": "Data saved successfully"}


@app.post("/process_url", response_model=Result)
async def process_url(item: Item):
    url = item.url
    extraction_result = scraper.extract_data(url)

    if "error" in extraction_result:
        raise HTTPException(status_code=400, detail=extraction_result["error"])
    
    web=dict(scraper.visit_url(item.url))
    text = web.get('website_text','')

    category: dict = text_classifier.predict(text)    

    image_bytes = extraction_result["image_bytes"]
    summary = text_classifier.summarize(text)
   

    image_base64 = base64.b64encode(image_bytes).decode('utf-8') if image_bytes else None

    return {"category": category, "summary": summary, "image_base64": image_base64}

@app.get("/search", response_model=SearchResults)
async def search_endpoint(keyword: str = Query(..., description="Keyword to search in URL and description")):
    results_from_db = mongo_handler.search_by_keyword(keyword)
    search_results = []
    for item in results_from_db:
        search_results.append(SaveRequest(
            url=item.get('url', ''),
            category=item.get('category'),
            summary=item.get('summary')
        ))

    return {"results": search_results}
