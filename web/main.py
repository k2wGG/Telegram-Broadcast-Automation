# web/main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from channel_db import get_channels, add_channel, remove_channel
from scheduler import schedule_post, start_scheduler
from datetime import datetime
import uvicorn
import os
import shutil
from fastapi import UploadFile, File

app = FastAPI()
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    channels = get_channels()
    return templates.TemplateResponse("index.html", {"request": request, "channels": channels})

@app.post("/add")
async def add(request: Request, channel_id: int = Form(...), name: str = Form("")):
    add_channel(channel_id, name)
    return RedirectResponse("/", status_code=302)

@app.post("/delete")
async def delete(request: Request, channel_id: int = Form(...)):
    remove_channel(channel_id)
    return RedirectResponse("/", status_code=302)

@app.post("/convert")
async def convert_post(request: Request, raw_text: str = Form(...)):
    from html import escape

    def convert_to_html(text: str) -> str:
        lines = text.splitlines()
        converted = []
        for line in lines:
            line = escape(line)

            # Простые замены (можно расширить)
            line = line.replace("**", "<b>").replace("__", "<i>")
            line = line.replace("➡️ ", '<a href="').replace("(", '">').replace(")", "</a>")
            converted.append(line)
        return "<br>\n".join(converted)

    html_result = convert_to_html(raw_text)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "html_result": html_result,
        "channels": get_channels()
    })


from fastapi import Form, File, UploadFile

@app.post("/schedule")
async def schedule(
    text: str = Form(...),
    time: str = Form(...),
    file: UploadFile = File(None)
):
    # обработка

    dt = datetime.strptime(time, "%Y-%m-%dT%H:%M")
    file_path = None

    if file and file.filename:
        upload_folder = "web/uploads"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    schedule_post(text, dt, file_path)
    return RedirectResponse("/", status_code=302)


if __name__ == "__main__":
    start_scheduler()
    uvicorn.run("web.main:app", host="0.0.0.0", port=8080, reload=True)
