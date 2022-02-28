import uvicorn
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv("local.env"))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        workers=1,
        reload=False,
    )
