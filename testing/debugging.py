import uvicorn
from fastapi import FastAPI

app_debug = FastAPI()


@app_debug.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


if __name__ == "__main__":
    uvicorn.run(app_debug, host="0.0.0.0", port=8000)


# DEBUGGING - connect degugger in editor with VScode or PyCharm
# Since you are running Uvicorn server directly from your code, you can call the python program directly from the debugger.
