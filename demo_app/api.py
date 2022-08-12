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
"""

import base64
import json
import math
from pathlib import Path
import pkg_resources
from random import random
import time

from tensorboardX import SummaryWriter
from webargs import fields, validate

from demo_app.misc import _catch_error, launch_tensorboard


BASE_DIR = Path(__file__).resolve().parents[1]


@_catch_error
def get_metadata():
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


def get_train_args():
    arg_dict = {
        "epoch_num": fields.Int(
            required=False,
            missing=10,
            description="Total number of training epochs",
        ),
    }
    return arg_dict


def train(**kwargs):
    """
    Dummy training. We just sleep for some number of epochs (1 epoch = 1 second)
    mimicking some computation taking place.
    We can log some random losses in Tensorboard to mimic monitoring.
    """
    logdir = BASE_DIR / "runs" / time.strftime("%Y-%m-%d_%H-%M-%S")
    writer = SummaryWriter(logdir=logdir)
    launch_tensorboard(logdir=logdir)
    for epoch in range(kwargs["epoch_num"]):
        time.sleep(1.)
        writer.add_scalar("scalars/loss", - math.log(epoch + 1), epoch)
    writer.close()

    return {"status": "done", "final accuracy": 0.9}


def get_predict_args():
    """
    TODO: add more dtypes
    * int with choices
    * composed: list of strs, list of int
    """
    # WARNING: missing!=None has to go with required=False
    # fmt: off
    arg_dict = {
        "demo-str": fields.Str(
            required=False,
            missing="some-string",
        ),
        "demo-str-choice": fields.Str(
            required=False,
            missing="choice2",
            enum=["choice1", "choice2"],
        ),
        "demo-int": fields.Int(
            required=False,
            missing=1,
        ),
        "demo-int-range": fields.Int(
            required=False,
            missing=50,
            validate=[validate.Range(min=1, max=100)],
        ),
        "demo-float": fields.Float(
            required=False,
            missing=0.1,
        ),
        "demo-bool": fields.Bool(
            required=False,
            missing=True,
        ),
        "demo-dict": fields.Str(  # dicts have to be processed as strings
            required=False,
            missing='{"a": 0, "b": 1}',  # use double quotes inside dict
        ),
        "demo-list-of-floats": fields.List(
            fields.Float(),
            required=False,
            missing=[0.1, 0.2, 0.3],
        ),
        "demo-image": fields.Field(
            required=False,
            type="file",
            location="form",
            description="image",  # description needed to be parsed by UI
        ),
        "demo-audio": fields.Field(
            required=False,
            type="file",
            location="form",
            description="audio",  # description needed to be parsed by UI
        ),
        "demo-video": fields.Field(
            required=False,
            type="file",
            location="form",
            description="video",  # description needed to be parsed by UI
        ),
    }
    # fmt: on
    return arg_dict


@_catch_error
def predict(**kwargs):
    """
    Return same inputs as provided. We also add additional fields
    to test the functionality of the Gradio-based UI [1].
       [1]: https://github.com/deephdc/deepaas_ui
    """
    # Dict are fed as str so have to be converted back
    kwargs["demo-dict"] = json.loads(kwargs["demo-dict"])

    # Add labels and random probalities to output as mock
    prob = [random() for _ in range(5)]
    kwargs["probabilities"] = [i / sum(prob) for i in prob]
    kwargs["labels"] = ["class2", "class3", "class0", "class1", "class4"]

    # Read media files and return them back in base64
    for k in ["demo-image", "demo-audio", "demo-video"]:
        with open(kwargs[k].filename, "rb") as f:
            media = f.read()
        media = base64.b64encode(media)  # bytes
        kwargs[k] = media.decode("utf-8")  # string (in utf-8)

    return kwargs


# Schema to validate the `predict()` output
schema = {
    "demo-str": fields.Str(),
    "demo-str-choice": fields.Str(),
    "demo-int": fields.Int(),
    "demo-int-range": fields.Int(),
    "demo-float": fields.Float(),
    "demo-bool": fields.Bool(),
    "demo-dict": fields.Dict(),
    "demo-list-of-floats": fields.List(fields.Float()),
    "demo-image": fields.Str(
        description="image"  # description needed to be parsed by UI
    ),
    "demo-audio": fields.Str(
        description="audio"  # description needed to be parsed by UI
    ),
    "demo-video": fields.Str(
        description="video"  # description needed to be parsed by UI
    ),
    "labels": fields.List(fields.Str()),
    "probabilities": fields.List(fields.Float()),
}
