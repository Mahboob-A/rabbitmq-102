import os, json 
from dotenv import load_dotenv
from typing import List, Dict, Tuple

import requests

load_dotenv()


class JobAPIHelper: 
    '''
        Helper class to interact with Linkedin API 
        '''
    RAPID_API_KEY = os.environ.get('RAPID_API_KEY')
    RAPID_API_HOST = os.environ.get('RAPID_API_HOST')

    print('RAPID_API_KEY: ', RAPID_API_KEY)
    def __make_request(
        self, request_url: str, payload: dict, headers: dict = None, params: dict = None
    ) -> List[Dict]:
        if headers is None: 
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": self.RAPID_API_KEY,
                "X-RapidAPI-Host": self.RAPID_API_HOST,
            }
        try: 
            print('payload: ', payload)
            response = requests.post(request_url, json=payload, headers=headers)
            #     print(f'\nresponse: {response.text}')
            print(f"\nresponse: {response.json()}")
            print(f'\nstatus code: {response.status_code}')
        except Exception as e: 
            print('[x] Error occurred.')
            err = {"error": e}
            print(err)

        return response

    def __get_linkedin_jobs(self, payload: dict) -> List[Dict]: 
        __request_url = "https://linkedin-jobs-search.p.rapidapi.com/"
        jobs = self.__make_request(request_url=__request_url, payload=payload)
        return jobs 

    def get_jobs(self, payload: dict) -> List[Dict]: 
        jobs = self.__get_linkedin_jobs(payload=payload)
        return  jobs  


jobs_api = JobAPIHelper()
