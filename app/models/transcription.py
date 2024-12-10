
from pydantic import BaseModel
from typing import Optional

from datetime import datetime
class SessionCreateResponse(BaseModel):
    session_id: str
    status: str = "active"
    start_time: datetime = datetime.utcnow()

class TranscriptionSaveRequest(BaseModel):
    session_id: str
    text: str
    is_final: bool = False

class SessionEndRequest(BaseModel):
    final_transcript: Optional[str] = None


class TranscriptionResponse(BaseModel):
    session_id: str
    text: str
    timestamp: datetime
    is_final: bool