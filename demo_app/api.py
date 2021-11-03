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
from functools import wraps
import json
import pkg_resources
from random import random

from aiohttp.web import HTTPBadRequest
from webargs import fields, validate


def _catch_error(f):
    """Decorate function to return an error as HTTPBadRequest, in case
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            raise HTTPBadRequest(reason=e)
    return wrap


def get_metadata():
    metadata = {
        "author": "Ignacio Heredia",
        "description": 
            """
            A minimal toy application for demo and testing purposes.
            We just implemented dummy inference, ie. we return the same inputs we are feed.
            """,
        "license": "MIT",
        "url": "https://github.com/deephdc/demo_app",
        "version": "0.1",
        "summary": 
            """
            Lorem Ipsum is simply dummy text of the printing and typesetting industry.
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
            when an unknown printer took a galley of type and scrambled it to make a type
            specimen book. It has survived not only five centuries, but also the leap into
            electronic typesetting, remaining essentially unchanged. It was popularised
            in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
            and more recently with desktop publishing software like Aldus PageMaker including
            versions of Lorem Ipsum.
            """,
    }
    return metadata


def get_predict_args():
    """
    TODO: add more dtypes
    * int with choices
    * composed: list of strs, list of int
    """
    # WARNING: missing!=None has to go with required=False
    arg_dict = {
        "demo-str": fields.Str(
            required=False,
            missing='some-string',
        ),
        "demo-str-choice": fields.Str(
            required=False,
            missing='choice2',
            enum=["choice1", "choice2"],
        ),
        "demo-int": fields.Int(
            required=False,
            missing=1,
        ),
        "demo-int-range": fields.Int(
            required=False,
            missing=50,
            validate=[validate.Range(min=1, max=100)]
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
            description="image",  # needed to be parsed by UI
        ),
        "demo-audio": fields.Field(
            required=False,
            type="file",
            location="form",
            description="audio",  # needed to be parsed by UI
        ),
        "demo-video": fields.Field(
            required=False,
            type="file",
            location="form",
            description="video",  # needed to be parsed by UI
        ),
    }
    
    return arg_dict


@_catch_error
def predict(**kwargs):
    """
    Return same inputs as provided. We also add additional fields
    to test the functionality of the Gradio-based UI [1].
       [1]: https://github.com/deephdc/deepaas_ui
    """
    # Dict are fed as str so have to be converted back
    kwargs['demo-dict'] = json.loads(kwargs['demo-dict'])

    # Add labels and random probalities to output as mock
    prob = [random() for _ in range(5)]
    kwargs['probabilities'] = [i / sum(prob) for i in prob]
    kwargs['labels'] = ['class2', 'class3', 'class0', 'class1', 'class4']
    
    # Read media files and return them back in base64
    for k in ['demo-image', 'demo-audio', 'demo-video']:
        with open(kwargs[k].filename, 'rb') as f:
            media = f.read()
        media = base64.b64encode(media)  # bytes
        kwargs[k] = media.decode('utf-8')  # string (in utf-8)
    
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
        description='image'),  # needed to be parsed by UI
    "demo-audio": fields.Str(
        description='audio'),  # needed to be parsed by UI
    "demo-video": fields.Str(
        description='video'),  # needed to be parsed by UI
    "labels": fields.List(fields.Str()),
    "probabilities": fields.List(fields.Float()),
}
