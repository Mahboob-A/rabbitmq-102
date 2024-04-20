from fastapi import FastAPI
from rabbitmq_helper import cloudamqp_jobconsumer
from api_center import jobs_api
import json
# from twilio_helper import twilio_api

app = FastAPI()


import traceback

def callback(ch, method, properties, body):
    try:
        print("callback")
        body = json.loads(body.decode("utf-8"))
        search_terms = body.get("job_search_text")
        location = body.get("job_location")
        email = body.get("email")

        payload = {"search_terms": search_terms, "location": location, "page": "1"}
        jobs = jobs_api.get_jobs(payload=payload)
        print(f"\n ALL JOBS: #{jobs} \n")
    except Exception as e:
        print(f"Error in callback function: {e}")
        traceback.print_exc()


def main():
    print('in main...')
    cloudamqp_jobconsumer.consume_jobs(callback=callback)


@app.on_event("startup")
def startup_event():
    main()


@app.on_event("shutdown")
def shutdown_event():
    pass
