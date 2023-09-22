from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from process_id_tool.process_id import ProcessManager
import uvicorn

class Process(BaseModel):
    process_name: str
    user_id: str

#initialize fast api app 
app = FastAPI()

#initialize Process Manager class
pm = ProcessManager()

@app.post("/processes/")
async def add_process_endpoint(process: Process):
    """Endpoint to add a process."""
    if not process.process_name:
        raise HTTPException(status_code=400, detail="process_name cannot be empty")
    if not process.user_id:
        raise HTTPException(status_code=400, detail="user_id cannot be empty")
    
    try:
        process_id = pm.add_process(process.process_name, process.user_id)
        return {"Process_ID": process_id}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.put("/processes/{pid}/{user_id}/{process_name}")
async def return_process_endpoint(pid: int, user_id: str, process_name: str):
    try:
        pm.return_process(pid, user_id, process_name)
        return {"detail": "Process returned successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/processes/{pid}/{user_id}")
async def get_process_endpoint(pid: int, user_id: str):
    """Endpoint to get a process. Or in other words, the state of a process."""
    try:
        process = pm.get_process(pid, user_id)
        return process
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)