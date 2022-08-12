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

import math
from pathlib import Path
import pkg_resources
import shutil
import tempfile
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
