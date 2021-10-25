Demo App
========

[![Build Status](https://jenkins.indigo-datacloud.eu/buildStatus/icon?job=Pipeline-as-code/DEEP-OC-org/demo_app/master)](https://jenkins.indigo-datacloud.eu/job/Pipeline-as-code/job/DEEP-OC-org/job/demo_app/job/master)

> :warning: This is **work-in-progress**.

A _minimal_ toy application for demo and testing purposes. We just implemented dummy inference, ie. we return the same inputs we are feed.

To launch it, first install the package then run deepaas:
```bash
git clone https://github.com/deephdc/demo_app && cd demo_app
pip install -e .
deepaas-run --listen-ip 0.0.0.0
```

> **TODOs**
> * implement additional data types
> * add dummy model metadata
> * create DEEP-OC repo to launch with Docker
