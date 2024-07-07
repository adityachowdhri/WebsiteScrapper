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


uri = "mongodb+srv://adityachowdhri123:tJbHc2PmElzsvLHN@webscraping.9rrm6xc.mongodb.net/?appName=WebScraping"

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
            sendEmail(link["_id"] , "kavitastarot@gmail.com", "hdkr mdjl bttz jcml", ["adityachowdhri123@gmail.com"], response)
            
    else:
        print(createNewRecord(documentInformation, link["_id"]))
        
        
def sendEmail(url, senderAddress, passkey, recievers, message):
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 
    smtp.ehlo() 
    smtp.starttls() 
    smtp.login(senderAddress, passkey)
    msg = MIMEMultipart() 
    msg['Subject'] = "Change to " + url  
    msg.attach(MIMEText(message))
    smtp.sendmail(from_addr=senderAddress, to_addrs=recievers, msg=msg.as_string()) 
    smtp.quit()


def createNewRecord(document, link):

    content = requests.get(link).text
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.body.get_text()
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text_bytes = cleaned_text.encode('utf-8')
    hash_object = hashlib.sha256(cleaned_text_bytes)
    hashed_text = hash_object.hexdigest()
    info = {"_id": link, "content": cleaned_text, "hash": hashed_text}
    document.insert_one(info)
    return info

def connectOutput():
    db_name = "WebScrappingInformation"
    db = client[db_name]

# Specify the collection name
    collection_name = "information"
    collection = db[collection_name]
    return collection

def connectInput():
    db_name = "WebScrappingInformation"
    db = client[db_name]

# Specify the collection name
    collection_name = "websites"
    collection = db[collection_name]
    return collection


