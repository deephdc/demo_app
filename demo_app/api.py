# -*- coding: utf-8 -*-

# Copyright 2021 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Integrate a model with the DEEP API

Inputs variables are configured via Python type hints.
Check [1][2] for a friendly introduction on type hints.

[1]: https://fastapi.tiangolo.com/python-types
[2]: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""

import base64
import json
import math
from pathlib import Path
import pkg_resources
from random import random
import time
from typing import Union

from tensorboardX import SummaryWriter
from typing_extensions import Annotated

from demo_app.misc import _catch_error, launch_tensorboard


BASE_DIR = Path(__file__).resolve().parents[1]

#TODO: remove fast api code when ready
from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/get_metadata")
@_catch_error
def get_metadata() -> dict:
    """
    DO NOT REMOVE - All modules should have a get_metadata() function
    with appropriate keys.
    """
    distros = list(pkg_resources.find_distributions(str(BASE_DIR), only=True))
    if len(distros) == 0:
        raise Exception("No package found.")
    pkg = distros[0]  # if several select first

    meta_fields = {
        "name": None,
        "version": None,
        "summary": None,
        "home-page": None,
        "author": None,
        "author-email": None,
        "license": None,
    }
    meta = {}
    for line in pkg.get_metadata_lines("PKG-INFO"):
        line_low = line.lower()  # to avoid inconsistency due to letter cases
        for k in meta_fields:
            if line_low.startswith(k + ":"):
                _, value = line.split(": ", 1)
                meta[k] = value

    return meta


# def get_train_args():
#     arg_dict = {
#         "epoch_num": fields.Int(
#             required=False,
#             missing=10,
#             description="Total number of training epochs",
#         ),
#     }
#     return arg_dict


@app.get("/train")
def train(
    epoch_num: int = 10,
) -> dict:
    """
    Dummy training. We just sleep for some number of epochs (1 epoch = 1 second)
    mimicking some computation taking place.
    We can log some random losses in Tensorboard to mimic monitoring.

    Parameters
    ----------
    * epoch_num : int (default 10)
        Total number of training epochs
    """
    logdir = BASE_DIR / "runs" / time.strftime("%Y-%m-%d_%H-%M-%S")
    writer = SummaryWriter(logdir=logdir)
    launch_tensorboard(logdir=logdir)
    for epoch in range(epoch_num):
        time.sleep(1.)
        writer.add_scalar("scalars/loss", - math.log(epoch + 1), epoch)
    writer.close()

    return {"status": "done", "final accuracy": 0.9}


# def get_predict_args():
#     """
#     TODO: add more dtypes
#     * int with choices
#     * composed: list of strs, list of int
#     """
#     # WARNING: missing!=None has to go with required=False
#     # fmt: off
#     arg_dict = {
#         "demo-str": fields.Str(
#             required=False,
#             missing="some-string",
#         ),
#         "demo-str-choice": fields.Str(
#             required=False,
#             missing="choice2",
#             enum=["choice1", "choice2"],
#         ),
#         "demo-int": fields.Int(
#             required=False,
#             missing=1,
#         ),
#         "demo-int-range": fields.Int(
#             required=False,
#             missing=50,
#             validate=[validate.Range(min=1, max=100)],
#         ),
#         "demo-float": fields.Float(
#             required=False,
#             missing=0.1,
#         ),
#         "demo-bool": fields.Bool(
#             required=False,
#             missing=True,
#         ),
#         "demo-dict": fields.Str(  # dicts have to be processed as strings
#             required=False,
#             missing='{"a": 0, "b": 1}',  # use double quotes inside dict
#         ),
#         "demo-list-of-floats": fields.List(
#             fields.Float(),
#             required=False,
#             missing=[0.1, 0.2, 0.3],
#         ),
#         "demo-image": fields.Field(
#             required=True,
#             type="file",
#             location="form",
#             description="image",  # description needed to be parsed by UI
#         ),
#         "demo-audio": fields.Field(
#             required=True,
#             type="file",
#             location="form",
#             description="audio",  # description needed to be parsed by UI
#         ),
#         "demo-video": fields.Field(
#             required=True,
#             type="file",
#             location="form",
#             description="video",  # description needed to be parsed by UI
#         ),
#     }
#     # fmt: on
#     return arg_dict

#TODO: how to upload file to the API
# https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile
#TODO: how to define the response type of the function
# https://fastapi.tiangolo.com/advanced/custom-response/#response
#TODO: variable description
# https://stackoverflow.com/questions/64364499/set-description-for-query-parameter-in-swagger-doc-using-pydantic-model-fastapi
#TODO: extra validation from FastAPI
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/



import pydantic

from pydantic import (
    BaseModel,
    NegativeFloat,
    NegativeInt,
    PositiveFloat,
    PositiveInt,
    NonNegativeFloat,
    NonNegativeInt,
    NonPositiveFloat,
    NonPositiveInt,
    conbytes,
    condecimal,
    confloat,
    conint,
    conlist,
    conset,
    constr,
    Field,
)

from enum import Enum

from typing import List, Dict, Literal

from pydantic import HttpUrl, Field




#TODO: remove
@app.post("/demo_route")
def demo_route(
    demo_dict1: Dict[str, float] = {"a": 2.0, "b": 1.5}

) -> dict:
    return locals()

# print(demo_route())


# from fastapi import UploadFile

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}


@app.post("/predict")
@_catch_error
def predict(
    # start with required parameters (ie. no default value)
    demo_str: str,  # string *without* default value

    # TESTS - string with description for users
    # name: Annotated[str, "This is a some parameter description that users might find helpful"],  # this doesn't show the description (in FastAPI), would need to be parsed by deepaas
    # name: str = Query(None, description="This is a some parameter description that users might find helpful"),  # this works but is FastAPI specific   

    # now add optional parameters (ie. have default value '=')
    demo_str1: str = "some-string",  # string
    demo_str2: Union[str, None] = None,  # string or None
    demo_str3: Literal["red", "blue"] = "blue",  # string, only from a given set of options
    demo_str4: Annotated[
        str,
        Field(description="This is a some parameter description that users might find helpful")
    ] = "some-string",  # add some description for the user
    demo_url: HttpUrl = "https://www.google.com",  # url

    demo_int: int = 1,  # int
    demo_int1: conint(gt=0, lt=10) = 5,  # int constrained to range [0,10]
    demo_float: float = 0.1,  # float

    demo_bool: bool = True,  # boolean

    demo_list: list = [0, "a", 2],  # arbitrary list
    demo_list1: List[int] = [0, 1, 2],  # list of integers

    demo_dict: dict = {'a': 1, 'b':2},  # dict
    demo_dict1: Dict[str, float] = {"a": 2.0, "b": 1.5},  # dict with specific format (keys are strings, values are float)
    ) -> dict:  # we return a dict
    """
    Return same inputs as provided. We also add additional fields
    to test the functionality of the Gradio-based UI [1].
       [1]: https://github.com/deephdc/deepaas_ui
    """
    # Return same inputs we are fed
    outputs = locals()

    # Add labels and random probalities to output as mock
    prob = [random() for _ in range(5)]
    outputs["probabilities"] = [i / sum(prob) for i in prob]
    outputs["labels"] = ["class2", "class3", "class0", "class1", "class4"]

    #todo: add back
    # # Read media files and return them back in base64
    # for k in ["demo-image", "demo-audio", "demo-video"]:
    #     with open(outputs[k].filename, "rb") as f:
    #         media = f.read()
    #     media = base64.b64encode(media)  # bytes
    #     outputs[k] = media.decode("utf-8")  # string (in utf-8)

    return outputs


# # Schema to validate the `predict()` output
# schema = {
#     "demo-str": fields.Str(),
#     "demo-str-choice": fields.Str(),
#     "demo-int": fields.Int(),
#     "demo-int-range": fields.Int(),
#     "demo-float": fields.Float(),
#     "demo-bool": fields.Bool(),
#     "demo-dict": fields.Dict(),
#     "demo-list-of-floats": fields.List(fields.Float()),
#     "demo-image": fields.Str(
#         description="image"  # description needed to be parsed by UI
#     ),
#     "demo-audio": fields.Str(
#         description="audio"  # description needed to be parsed by UI
#     ),
#     "demo-video": fields.Str(
#         description="video"  # description needed to be parsed by UI
#     ),
#     "labels": fields.List(fields.Str()),
#     "probabilities": fields.List(fields.Float()),
# }
