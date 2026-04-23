from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fanar_nlu import fanar_nlu
from router import route_nlu_result

app = FastAPI(title="Viora NLU Server", description="Port 8000: Text Intent Analysis")

class QueryRequest(BaseModel):
    text: str

@app.post("/api/v1/parse")
async def parse_command(request: QueryRequest):
    try:
        nlu_result = fanar_nlu(request.text)
        decision, payload = route_nlu_result(nlu_result)
        
        return {
            "status": "success",
            "decision": decision,
            "nlu": {
                "viora_reply": payload.viora_response,
                "intent": payload.intent,
                "confidence": payload.confidence,
                "entities": payload.entities.model_dump(), # Using full null mapping
                "needs_clarification": payload.needs_clarification
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # NLU stays on 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)