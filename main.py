from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import AfterValidator, BaseModel


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


### Request Body

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    item_dict = item.dict()
    item_dict.update({"item_id": item_id})
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    if q:
        item_dict.update({"q": q})
    return item_dict

### Query Param Validation

@app.get("/specific-query")
async def specific_query(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None):
    return {"Query": q}

@app.get("/query-list")
async def query_list(q: Annotated[list[str] | None, Query()] = None):
    return q

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

@app.get("/custom-query-validation")
async def custom_query_validation(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

### Path Param Validation

@app.get("/paths/{path_id}")
async def path_validation(
    path_id: Annotated[int, Path(title="The ID of the item to get")]
):
    return {"path_id": path_id}

### Python magic

@app.get("/python-magic/{id}")
async def python_magic(*, id: int = Path(title="BumBum who reads it"), q: str):
    """
    Python won't do anything with that *, but it will know that all the following parameters should be called as keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
    """
    return {
        "id": id,
        "q": q
    }

### Numeric validations

@app.get("/path-num-validation/{item_id}")
async def path_num_validation(item_id: Annotated[int, Path(title="dfhufhjfhur", gt=1, le=100)]):
    return {"item_id": item_id}
