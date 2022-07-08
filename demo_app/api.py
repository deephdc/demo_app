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

from functools import wraps
import shutil
import tempfile

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
            We just implemented dummy inference, ie. we return the
            same inputs we are feed.
            """,
        "license": "MIT",
        "url": "https://github.com/deephdc/demo_app",
        "version": "0.1",
        "summary":
            """
            Lorem Ipsum is simply dummy text of the printing and
            typesetting industry. Lorem Ipsum has been the industry's
            standard dummy text ever since the 1500s, when an unknown
            printer took a galley of type and scrambled it to make a
            type specimen book. It has survived not only five centuries,
            but also the leap into electronic typesetting, remaining
            essentially unchanged. It was popularised in the 1960s with
            the release of Letraset sheets containing Lorem Ipsum
            passages, and more recently with desktop publishing software
            like Aldus PageMaker including versions of Lorem Ipsum.
            """,
    }
    return metadata


def get_predict_args():
    """
    Input fields for the user.
    """
    arg_dict = {
        "demo-image": fields.Field(
            required=False,
            type="file",
            location="form",
            description="image",  # needed to be parsed by UI
        ),
        # Add format type of the response of predict()
        # For demo purposes, we allow the user to receive back
        # either an image or a zip containing an image.
        # More options for MIME types: https://mimeapplication.net/
        "accept": fields.Str(
            description="Media type(s) acceptable for the response.",
            validate=validate.OneOf(["image/*", "application/zip"]),
        ),
    }
    return arg_dict


@_catch_error
def predict(**kwargs):
    """
    Return same inputs as provided.
    """
    filepath = kwargs['demo-image'].filename

    # Return the image directly
    if kwargs['accept'] == 'image/*':
        return open(filepath, 'rb')

    # Return a zip
    elif kwargs['accept'] == 'application/zip':

        zip_dir = tempfile.TemporaryDirectory()

        # Add original image to output zip
        shutil.copyfile(filepath,
                        zip_dir.name + '/demo.png')

        # Add for example a demo txt file
        with open(f'{zip_dir.name}/demo.txt', 'w') as f:
            f.write('Add here any additional information!')

        # Pack dir into zip and return it
        shutil.make_archive(
            zip_dir.name,
            format='zip',
            root_dir=zip_dir.name,
        )
        zip_path = zip_dir.name + '.zip'

        return open(zip_path, 'rb')
