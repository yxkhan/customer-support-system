# import httpx

# url = "https://a0858bf8-1e58-451d-90a9-c1553328a026-us-east-2.apps.astra.datastax.com"
# try:
#     res = httpx.get(url, timeout=10)
#     print("Connected! Status:", res.status_code)
# except Exception as e:
#     print("❌ Failed to connect:", e)

from dotenv import load_dotenv
import os
load_dotenv()

print("Loaded endpoint:", os.getenv("ASTRA_DB_API_ENDPOINT"))

