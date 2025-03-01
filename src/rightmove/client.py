import asyncio
import random
import time
from typing import List

import aiohttp
import requests

from .models import Property


class RightmoveAPI:
    def __init__(self, api_url: str = "https://www.rightmove.co.uk/house-prices/api/sold-properties",
                 rate: float = 1.0, jitter: float = 0.5):
        self.api_url = api_url
        self.response_data = {}
        self.rate = rate
        self.jitter = jitter

    def manage_request_rate(self):
        time_to_sleep = self.rate + self.jitter * (2 * random.random() - 1)
        time.sleep(time_to_sleep)

    def fetch_data(self, location_identifier: str, sold_in: int = 20):
        params = {
            "location": location_identifier,
            "soldIn": sold_in
        }

        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            self.response_data[location_identifier] = response.json()
        else:
            response.raise_for_status()

    async def fetch_data_by_postcodes(
            self, postcodes: list, sold_in: int = 20, radius: float = 0.5) -> List[Property]:
        response_data = []
        tasks = []
        for postcode in postcodes:
            params = {
                "location": postcode,
                "soldIn": sold_in,
                "radius": radius,
            }
            tasks.append(self.fetch_data_for_params(params))

        results = await asyncio.gather(*tasks)
        for result in results:
            response_data.extend(result)

        return response_data

    async def fetch_data_for_params(self, params: dict) -> List[Property]:
        page = 1
        response_data = []
        has_next_page = True

        while has_next_page:
            params["pageNumber"] = page
            retry_count = 0
            successfull_request = False
            while retry_count < 5 and not successfull_request:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.api_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            response_data.extend(data['properties'])
                            last_page = data['pagination']['last']
                            print(f"""Fetched page {page} out of {
                                last_page} for params: {params}""")

                            if data['pagination']['current'] >= data['pagination']['last']:
                                has_next_page = False
                            page += 1
                            successfull_request = True
                        else:
                            print(
                                f"Failed to fetch page {page} for params: {params}")
                            print(f"Status code: {response.status}")
                            print(response.url)
                            print(await response.text())
                            print()
                            retry_count += 1
                            # Exponential backoff: 1, 2, 4, 8, 16 seconds
                            await asyncio.sleep(2 ** retry_count)
                            if retry_count == 5:
                                response.raise_for_status()

                # Add a delay between requests to avoid spamming the server
                await asyncio.sleep(self.rate + self.jitter * (2 * random.random() - 1))

        properties = [Property(**property_data)
                      for property_data in response_data]
        return properties
