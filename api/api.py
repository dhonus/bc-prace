# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# https://fastapi.tiangolo.com/tutorial/body/
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# this is required to be able to access the fastapi server from VUE.js on another port
from fastapi.middleware.cors import CORSMiddleware

from core.Parser import Parser, EmptyInputException, InvalidExpressionException
from core.Evaluator import Evaluator
import logging
from typing import List
import main
import git


class Item(BaseModel):
    existential: dict[str, list[str]] = {}
    universal: List[str] = []
    valid: bool | None = None
    notes: str = ""


class Thing(BaseModel):
    predicates: List[str]
    conclusion: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://10.0.0.117:8000", "http://130.162.49.62:8080"],  # frontend address
    #allow_origins=['*'],  # frontend address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api", response_model=Item)
async def send_expression(item: Thing):
    logging.root.setLevel(logging.DEBUG)

    predicates = [predicate.replace(" ", "") for predicate in item.predicates]

    p_index = 1
    try:
        trees = []
        for predicate in predicates:
            print(f"{predicate}:")
            parser = Parser(predicate)
            tree = parser.parse()
            trees.append(tree)
            print(tree.print())
            print()

        parser = Parser(item.conclusion)
        conclusion_tree = parser.parse()
        conclusion_tree.validate()

        trees = sorted(trees, key=lambda tr: tr.value)  # sort to have universal statements first

        evaluator = Evaluator()
        solution = evaluator.eval(trees, conclusion_tree)
        validity = evaluator.validity(solution)
        print(f"\n\n----------\nsolution: {solution}\n----------")
        print(validity)

        p_index += 1

    except InvalidExpressionException as iee:
        print(iee)
    except EmptyInputException as e:
        responseItem = Item()
        responseItem.notes = "Prázdný vstup, nebo chybějící závěr."
        return responseItem
    except Exception as e:
        logging.critical(f"{type(e).__name__}: V {p_index}. premise: {e}")
        responseItem = Item()
        responseItem.notes = f"{type(e).__name__}: V {p_index}. premise: {e}"
        return responseItem

    responseItem = Item()
    responseItem.existential = solution.get('Exists within')
    responseItem.universal = list(solution.get('Crossed out'))
    responseItem.valid = validity
    responseItem.notes = "OK"

    return responseItem


@app.get("/")
def home():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    import time

    time.asctime(time.gmtime(repo.head.object.committed_date))
    tim = time.strftime("%d. %m. %Y %H:%M", (time.gmtime(repo.head.object.committed_date)))
    return f"Připojeno. Hash aktivní verze z {tim} UTC je {sha}."
