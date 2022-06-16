Demo App
========

[![Build Status](https://jenkins.indigo-datacloud.eu/buildStatus/icon?job=Pipeline-as-code/DEEP-OC-org/demo_app/master)](https://jenkins.indigo-datacloud.eu/job/Pipeline-as-code/job/DEEP-OC-org/job/demo_app/job/master)

A _minimal_ toy application for demo and testing purposes. We just implemented dummy inference, ie. we return the same inputs we are fed. If some input is not fed we generate a default one.

To launch it, first install the package then run [deepaas](https://github.com/indigo-dc/DEEPaaS):
```bash
git clone https://github.com/deephdc/demo_app 
cd demo_app
pip install -e .
deepaas-run --listen-ip 0.0.0.0
```
The associated Docker container for this module can be found in [deephdc/DEEP-OC-demo_app](https://github.com/deephdc/DEEP-OC-demo_app).

Samples for media files are provided in `./data`.

The two branches in this repo cover the two main usecases:
* [master](https://github.com/deephdc/demo_app/blob/master/demo_app/api.py): this is a reference implementation on how to return a JSON response for `predict()`.
* [return-files](https://github.com/deephdc/demo_app/blob/return-files/demo_app/api.py): this is a reference implementation on how to return non-JSON responses for `predict()`. This is particularly useful when returning:
     - long responses (that could better fit better in a `txt` file), 
     - media files (eg. returning an image),
     - multiple files (for example returning an image and a text file at the same time, packing them into a zip file).

> TODO: Add one more branch with tox tests, to test Jenkisnfile functionality.
