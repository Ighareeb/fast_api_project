from fastapi import BackgroundTasks, FastAPI, Depends

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


def write_log(email: str, message=""):
    with open("log.txt", mode="a") as log:
        content = f"notification for {email}: {message}"
        log.write(content)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send_notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Notification sent in the background"}
    # background_tasks.add_task(write_notification, email, message='some notification')
    # return {'message': 'Notification sent in the background'}


# Define tasks to be run after returning a respoinse - useful for ops that happen after a request but client doesnt have to wait for to get response (eg. email notifications, processing data - send Accepted res and process in background)
