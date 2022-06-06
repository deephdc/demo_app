Demo App
========

[![Build Status](https://jenkins.indigo-datacloud.eu/buildStatus/icon?job=Pipeline-as-code/DEEP-OC-org/demo_app/master)](https://jenkins.indigo-datacloud.eu/job/Pipeline-as-code/job/DEEP-OC-org/job/demo_app/job/master)

A _minimal_ toy application for demo and testing purposes. We just implemented dummy inference, ie. we return the same inputs we are feed. If some input is not feed we generate a default one.

To launch it, first install the package then run deepaas:
```bash
git clone https://github.com/deephdc/demo_app && cd demo_app
pip install -e .
deepaas-run --listen-ip 0.0.0.0
```
The associated Docker container for this module can be found in [deephdc/DEEP-OC-demo_app](https://github.com/deephdc/DEEP-OC-demo_app).

Samples for media files are provided in `./data`.
