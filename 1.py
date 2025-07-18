# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "fastapi>=0.104.1",
#     "uvicorn>=0.24.0", 
#     "httpx>=0.25.2",
# ]
# ///


"""
Write a FastAPI proxy server that serves the data from the given URL but also adds a CORS header Access-Control-Allow-Origin: * to the response.

For example, if your API URL endpoint is http://127.0.0.1:8000/api, then a request to http://127.0.0.1:8000/api?url=https%3A%2F%2Fexample.com%2F%3Fkey%3Dvalue should return the data from https://example.com/?key=value but with the CORS header.

Note: Keep your server running for the duration of the exam.

What is your FastAPI Proxy URL endpoint?
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
# add cores to the API
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api")
async def proxy(request: Request):
    url = request.query_params.get("url")
    if not url:
        return JSONResponse(status_code=400, content={"error": "Missing 'url' query parameter"})

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            print(response.content)
            return JSONResponse(
                content=response.content,
                headers={"Access-Control-Allow-Origin": "*"}
            )
    except httpx.RequestError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    except httpx.HTTPStatusError as e:
        return JSONResponse(status_code=e.response.status_code, content={"error": str(e)})
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
