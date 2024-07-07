import requests
from bs4 import BeautifulSoup
import re
import hashlib
import ollama
import hashlib
import urllib.request
import urllib.error
import smtplib 
import urllib.parse
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
import time 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from helper import *

uri = os.getenv("DATABASE_URL")
emailId = os.getenv("EMAIL_ID")
passkey = os.getenv("EMAIL_PASSKEY")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))



documentInformation = connectOutput()    
documentLinks = connectInput()
for link in documentLinks.find():
    if documentInformation.find_one({ "_id": link["_id"] }) is not None:
        doc = documentInformation.find_one({ "_id": link["_id"] })
        content = requests.get(doc["_id"]).text
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.body.get_text()
        cleaned_text = re.sub(r'\s+', ' ', text)
        cleaned_text_bytes = cleaned_text.encode('utf-8')
        hash_object = hashlib.sha256(cleaned_text_bytes)
        hashed_text = hash_object.hexdigest()
        if hashed_text == doc["hash"]:
            print("No Change")
        else:
            print("Change")
            old_text = doc["content"]
            question = f"""What is the difference in words between these texts: Text 1: {cleaned_text} Text 2: {old_text}"""
            response = ollama.generate(model='llama3', prompt=question)
            sendEmail(link["_id"] , emailId, passkey, ["adityachowdhri123@gmail.com"], response)
            
    else:
        print(createNewRecord(documentInformation, link["_id"]))
        
        


