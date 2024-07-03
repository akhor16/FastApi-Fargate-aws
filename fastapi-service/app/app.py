from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError
import uuid

app = FastAPI()

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('MessagesTable')


class Message(BaseModel):
    message: str


@app.post("/messages")
async def create_message(msg: Message):
    message_id = str(uuid.uuid4())
    try:
        table.put_item(Item={'id': message_id, 'message': msg.message})
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Failed to save message")
    return {"id": message_id}


@app.get("/messages/{message_id}")
async def get_message(message_id: str):
    try:
        response = table.get_item(Key={'id': message_id})
    except ClientError as e:
        raise HTTPException(status_code=500, detail="Failed to fetch message")

    item = response.get('Item')
    if not item:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": item['message']}
