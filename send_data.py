from apscheduler.schedulers.background import BackgroundScheduler
from db import Detection
import requests

def send():
    query = Detection.select()
    response = requests.head('https://httpbin.org/get')
    
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send, 'interval', minutes=1)
    scheduler.start()
