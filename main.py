from flask import Flask
import asyncio
import httpx
import time

app = Flask(__name__)


async def send_async_request(url):
    """"Function to handle asynchronous requests"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()


async def execute_jokes_request(url, number_of_requests):
    """"Function to create a batch request based on the amount of request that we need and formatted with the necessary attributes"""
    responses = await asyncio.gather(*[send_async_request(url) for _ in range(number_of_requests)])
    formatted_responses = []
    for response in responses:
        formatted_responses.append({"id": response["id"], "value": response["value"], "url": response["icon_url"]})
    return formatted_responses


@app.route("/get-jokes", methods=['GET'])
async def get_jokes():
    jokes_to_request = 25
    retries = 0
    url = "https://api.chucknorris.io/jokes/random"
    unique_jokes = []
    start = time.time()
    # Added retries variable to have a maximum of retries for the requests
    while jokes_to_request > 0 and retries < 10:
        responses = await execute_jokes_request(url, jokes_to_request)
        response_ids = [obj["id"] for obj in responses]
        unique_jokes_ids = set(response_ids)
        unique_jokes.extend([j for j in responses if j["id"] in unique_jokes_ids])
        jokes_to_request = jokes_to_request - len(unique_jokes_ids)
        retries += 1

    end = time.time()

    return {"time": f"{end - start}s", "jokes": unique_jokes}


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)
