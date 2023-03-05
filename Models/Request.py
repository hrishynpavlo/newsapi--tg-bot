from pydantic import BaseModel

class Chat(BaseModel):
    id: int
    username: str

class Message(BaseModel):
    message_id: int
    chat: Chat
    text: str

class CallbackQuery(BaseModel):
    id: str
    data: str
    message: Message

class UpdateRequest(BaseModel):
    update_id: int
    callback_query: CallbackQuery | None
    message: Message | None