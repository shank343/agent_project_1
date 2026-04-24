from fastapi import FastAPI
from pydantic import BaseModel
from multi_agent_research_system import create_research_system

app = FastAPI()
research_system = create_research_system()

class TopicRequest(BaseModel):
    topic: str

@app.post("/research")
def run_research(request: TopicRequest):
    result = research_system.invoke({
        "messages": [],
        "topic": request.topic,
        "search_queries": [],
        "findings": [],
        "analysis": "",
        "report": "",
        "quality_score": 0.0,
        "quality_feedback": "",
        "iteration": 0,
    })
    return {
        "report": result["report"],
        "quality_score": result["quality_score"],
        "iterations": result["iteration"]
    }