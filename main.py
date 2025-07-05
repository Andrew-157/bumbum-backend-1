from enum import Enum

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello BumBum"}


### Path Parameters
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

### Query Parameters

fake_bumbums_db = [ # In reality, nothing is ever fake about BumBums...
        {"bumbum_name": "King"},
        {"bumbum_name": "Emperor"},
        {"bumbum_name": "President"},
]

@app.get("/bumbums/")
async def read_bumbums(skip: int = 0, limit: int = 10):
    return fake_bumbums_db[skip : skip + limit]


@app.get("/bumbums/optional-query")
async def read_bumbum_optional_query(q: str | None = None):
    response = {"message": "bumbum"}
    if q:
        response["query"] = q
    return response

@app.get("/bumbums/bool-query")
async def read_bumbum_bool_query(short: bool = False):
    """
    http://127.0.0.1:8000/bumbums/bool-query?short=false(any case variation, that is False, fAlse, etc.) - results into short being False
    http://127.0.0.1:8000/bumbums/bool-query?short=0 - results into short being False
    http://127.0.0.1:8000/bumbums/bool-query?short=off(any case variation) - results into short being False

    The opposites result in True

    Any other value results in error
    """
    return {
        "message": f"What this bumbumless heretic says is {short}"
    }

@app.get("/bumbums/{bumbum_id}/items/{item_id}")
async def read_bumbum_item(
    bumbum_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": bumbum_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is an amazing item with long description."
            }
        )
    return item

@app.get("/bumbums/required-query")
async def read_bumbum_required_query(needy: str):
    return {"message": f"BumBum needs that query: {needy}"}

class BumBumRankFormat(str, Enum):
    title = "title"
    upper = "upper"
    lower = "lower"

@app.get("/bumbums/{bumbum_id}/rank/{rank_id}")
async def read_bumbum_tone_of_queries(bumbum_id: int, rank_id: str, rank_division: int, rank_format: BumBumRankFormat, description: str | None = None):
    response = {
        "bumbum_id": bumbum_id
    }
    formatted_rank_id = rank_id
    if rank_format == BumBumRankFormat.title:
        response["rank_id"] = rank_id.title()
    elif rank_format == BumBumRankFormat.upper:
        response["rank_id"] = rank_id.upper()
    elif rank_format == BumBumRankFormat.lower:
        response["rank_id"] = rank_id.lower()
    response["rank_division"] = rank_division
    if description:
        response["description"] = description
    return response
