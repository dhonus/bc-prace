# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# https://fastapi.tiangolo.com/tutorial/body/
from fastapi import FastAPI, Query
from pydantic import BaseModel
# this is required to be able to access the fastapi server from VUE.js on another port
from fastapi.middleware.cors import CORSMiddleware

from core.Parser import Parser, EmptyInputException, InvalidExpressionException
from core.Evaluator import Evaluator
import logging
from typing import List
import main


class Item(BaseModel):
    existential: dict
    universal: dict
    universe: str
    notes: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # frontend address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api")
async def send_expression(item: Item, conclusion: str,  predicates: List[str] = Query(None)):

    logging.root.setLevel(logging.DEBUG)

    predicates = [predicate.replace(" ", "") for predicate in predicates]

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

        parser = Parser(conclusion)
        conclusion_tree = parser.parse()

        trees = sorted(trees, key=lambda tr: tr.value)  # sort to have universal statements first

        evaluator = Evaluator()
        solution = evaluator.eval(trees, conclusion_tree)
        print(f"\n\n----------\nsolution: {solution}\n----------")

        p_index += 1

    except EmptyInputException:
        pass
    except InvalidExpressionException as iee:
        print(iee)
    except Exception as e:
        logging.critical(f"{type(e).__name__}: In predicate {p_index}: {e}")
    item.existential = solution.get('Exists within')
    item.universal = solution.get('Crossed out')
    item.universe = "none"
    item.notes = "OK"
    return item


@app.get("/")
def home():
    return f"Připojeno. Aktivní verze {main.ACTIVE_VERSION_ID}"
