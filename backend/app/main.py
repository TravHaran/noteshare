from turtle import up
from fastapi import FastAPI, Body, Request, File, UploadFile, Form, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .routers import auth, book, comment, library, user, follow, notification
from .routers import patron, patron_invite, patron_request, tag, vote_book, vote_comment
from .database import engine, SessionLocal
from .config import settings
import uuid
from PyPDF2 import PdfMerger, PdfReader
import os
# to start server run CL: uvicorn app.main:app
# to start server and monitor code changes run CL: uvicorn main:app --reload

templates = Jinja2Templates(directory="../../test_frontend")
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(book.router)
app.include_router(comment.router)
app.include_router(follow.router)
app.include_router(library.router)
app.include_router(notification.router)
app.include_router(patron.router)
app.include_router(patron_invite.router)
app.include_router(patron_request.router)
app.include_router(tag.router)
app.include_router(user.router)
app.include_router(vote_book.router)
app.include_router(vote_comment.router)


@app.get("/")
async def root():
    return {"message": "Welcome to NoteShare!"}


@app.get("/home/{user_name}", response_class=HTMLResponse)
def write_home(request: Request, user_name: str):
    return templates.TemplateResponse("home.html", {"request": request, "username": user_name})


@app.post("/submitform")
async def handle_form(files: list[UploadFile] = File(...),):
    uploaded_files = []
    for file in files:
        print(file.filename)
        if file.filename.endswith(".pdf") == False:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail="unsupported file-type, please upload a pdf")
        filename = str(uuid.uuid4()) + ".pdf"
        content = await file.read()
        if len(files) > 1:
            file_location = f"{settings.waiting_room_file_dir}/{filename}"
        else:
            # save in database
            file_location = f"{settings.file_dir}/{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(content)
        uploaded_files.append(file_location)

    if len(uploaded_files) > 1:
        merger = PdfMerger()
        for pdf in uploaded_files:
            merger.append(pdf)
        filename = str(uuid.uuid4()) + ".pdf"
        file_location = f"{settings.file_dir}/{filename}"  # save in database
        merger.write(file_location)
        merger.close()
        # remove the files that were in the waiting room
        for file in uploaded_files:
            os.remove(file)
    pdf_file = PdfReader(file_location)
    page_count = len(pdf_file.pages)
    print(page_count)  # save in database
    return {"uploaded_file": file_location, "page_count": page_count}
