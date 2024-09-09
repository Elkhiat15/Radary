from fastapi import FastAPI,File, UploadFile, Body

from fastapi.responses import JSONResponse
import analyser, summarizer

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/analyse_accident")
async def analyse_accident(image: UploadFile = File(...)):
    description, authority, level = analyser.analyse_accident(image)
    return JSONResponse(content={"description": description, "authority": authority, "level":level }, media_type="application/json")

@app.post("/analyse_eco-issue")
async def analyse_isuue(image: UploadFile = File(...)):
    description, authority, priority = analyser.analyse_isuue(image)
    return JSONResponse(content={"description": description, "authority": authority, "priority":priority }, media_type="application/json")

@app.post("/summarize_feedbacks")
async def summarize_feedbacks(feedbacks: list[str] = Body(...)):
    x = summarizer.summarize(feedbacks)
    return JSONResponse(content={"summary": x}, media_type="application/json")