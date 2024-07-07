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

emailId = os.getenv("EMAIL_ID")
passkey = os.getenv("EMAIL_PASSKEY")




while True:
    time.sleep(3)
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
                continue 
            else:
                print("Change")
                filter = {"_id": link["_id"]}
                update = {
                    "$set": {
                        "content": cleaned_text,
                        "hash": hashed_text
                    }
                }
                result = documentInformation.update_one(filter, update)
                if result.modified_count > 0:
                    print("Document updated successfully.")
                else:
                    print("No documents matched the filter. No updates were made.")
                old_text = doc["content"]
                question = f"""What is the difference in words between these texts: Text 1: {cleaned_text} Text 2: {old_text}"""
                response = ollama.generate(model='llama3', prompt=question)
                print("The response is: ", response)
                sendEmail(link["_id"] , emailId, passkey, ["adityachowdhri123@gmail.com"], response)


                
        else:
            print(createNewRecord(documentInformation, link["_id"]))
            
        


