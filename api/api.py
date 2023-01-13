# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# https://fastapi.tiangolo.com/tutorial/body/
from __future__ import annotations

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
    existential: dict[str, set[tuple]] = {}
    bad: dict[str, set[tuple]] = {}
    universal: set[tuple] = set()
    explanations: dict[int, list[str]] = {}
    predicates: dict[int, str] = {}
    sets: List[str] = []
    valid: bool | None = None
    notes: str = "OK"
    steps: list[Item] = []
    p_index: int = 0


class Thing(BaseModel):
    predicates: List[str]
    conclusion: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://10.0.0.117:8000",
        "http://130.162.49.62:8080",
    ],  # frontend address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api", response_model=Item)
async def send_expression(item: Thing):
    logging.root.setLevel(logging.DEBUG)

    predicates = [predicate.replace(" ", "") for predicate in item.predicates]

    # we will return the enumerated predicates to the frontend to make sure the order is maintained
    predicates_to_return = {}

    p_index = 1
    try:
        responseItem = Item()
        trees = []
        parser = Parser()
        for predicate in predicates:
            predicates_to_return[p_index] = predicate
            parser.attach(predicate, p_index)
            tree = parser.parse()
            tree.validate()
            trees.append(tree)
            print(tree.print())
            print()
            p_index += 1

        predicates_to_return[p_index] = item.conclusion
        parser.attach(item.conclusion, p_index)
        conclusion_tree = parser.parse()
        conclusion_tree.validate()

        trees = sorted(
            trees, key=lambda tr: tr.value
        )  # sort to have universal statements first

        print(trees, "trees")

        evaluator = Evaluator()
        solution = evaluator.eval(trees, conclusion_tree)
        responseItem.sets += evaluator.get_sets()
        validity = evaluator.validity(solution)
        responseItem.sets += evaluator.get_sets()
        responseItem.explanations = evaluator.get_explanations()
        responseItem.sets = list(set(responseItem.sets))
        responseItem.predicates = predicates_to_return

        for step in evaluator.get_steps():
            item = Item()
            item.sets = evaluator.get_sets()
            print(f'problematic {step["Exists within"]}')
            item.existential = step["Exists within"]
            item.universal = step["Crossed out"]
            item.explanations = step["Explanations"]
            item.p_index = step["Predicate"]
            item.bad = step["Bad"]
            responseItem.steps.append(item)

        print(evaluator.get_sets(), "aaa")
        print(f"\n\n----------\nsolution: {solution}\n----------")
        print(validity)
        print(f"predicated to return {predicates_to_return}")

    except InvalidExpressionException as iee:
        print(iee)
    except EmptyInputException as e:
        responseItem = Item()
        responseItem.notes = "Prázdný vstup, nebo chybějící závěr!"
        return responseItem
    except Exception as e:
        responseItem = Item()
        if p_index == len(predicates) :
            logging.critical(f"{type(e).__name__}: V {p_index}. premise: {e}")
            responseItem.notes = f"Chyba v {p_index}. premise: {e}"
        else:
            logging.critical(f"{type(e).__name__}: V závěru: {e}")
            responseItem.notes = f"Chyba v závěru: {e}"

        return responseItem

    responseItem.existential = solution.get("Exists within")
    responseItem.universal = list(solution.get("Crossed out"))
    responseItem.valid = validity

    return responseItem


@app.get("/")
def home():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    import time

    time.asctime(time.gmtime(repo.head.object.committed_date))
    tim = time.strftime(
        "%d. %m. %Y %H:%M", (time.gmtime(repo.head.object.committed_date))
    )
    return f"Připojeno. Hash aktivní verze z {tim} UTC je {sha}."
