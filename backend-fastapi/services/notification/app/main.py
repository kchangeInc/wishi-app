from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class NotifyRequest(BaseModel):
    cluster_id: int
    message: str
    recipients: list[str]

class NotifyResponse(BaseModel):
    status: str
    delivered_to: int
    timestamp: datetime

@app.post("/notify", response_model=NotifyResponse)
def notify(req: NotifyRequest):
    # TODO: integrate with real notification service (FCM/email/sms)
    print(f"[Notification] -> cluster={req.cluster_id} message={req.message} recipients={req.recipients}")
    return NotifyResponse(status="ok", delivered_to=len(req.recipients), timestamp=datetime.utcnow())
