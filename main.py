from enum import Enum

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello BumBum"}


@app.get("/bumbum/me")
async def get_bumbum_me():
    return {"message": "Current BumBum for you"}


@app.get("/bumbum/{bumbum_id}")
async def get_bumbum(bumbum_id: int):
    return {"bumbum_id": bumbum_id}


class BumBumModel(str, Enum):
    root = "root"
    special = "special"
    hidden = "hidden"

BumBumModelToMessage = {
    BumBumModel.root: "ROOT OF ALL BUMBUMS",
    BumBumModel.special: "My special BumBum",
    BumBumModel.hidden: "Where are you, BumBum?"
}

@app.get("/bumbum/models/{model_name}")
async def get_model_bumbum(model_name: BumBumModel):
    # FastAPI won't allow model_name to be anything not in BumBumModel
    return {"model_name": model_name, "message": BumBumModelToMessage[model_name]}


@app.get("/bumbum/archive/{file_path:path}") # URL path would be something like:
async def read_bumbum_archive(file_path: str):
    """
    url could look like this: http://127.0.0.1:8000/bumbum/archive/bumbum.tar.gz
    and the response would look like this:
        {
          "WARNING": "IN THE BUMBUM ARCHIVE SHALT NOT ENTER THOSE WHO KNOW NO BUMBUM",
          "file_path": "bumbum.tar.gz"
        }
    OR url could look like this: http://127.0.0.1:8000/bumbum/archive//root/bumbum.tar.gz
    and the response would look like this:
        {
            "WARNING": "IN THE BUMBUM ARCHIVE SHALT NOT ENTER THOSE WHO KNOW NO BUMBUM",
            "file_path": "/root/bumbum.tar.gz"
        }
    """
    return {
            "WARNING": "IN THE BUMBUM ARCHIVE SHALT NOT ENTER THOSE WHO KNOW NO BUMBUM",
            "file_path": file_path
    }
