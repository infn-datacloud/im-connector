# IM Connector

## Overview

This code is a middleware component creating an interface to an InfrastructureManager instance.
Currently, it exposes a 1:1 replica of the IM REST API and accepts the exact same requests as the IM.
To achieve this, this code consists of two components:

- the IM Adapter, responsible for parsing the incoming requests into an OO representation
- the IM Client, responsible for sending the parsed request to the IM and to relay the IM response back to the caller

The API replica is served by a FastAPI app, which in turn relies on a separate library to construct the actual requests.

Further implementation details are provided in the [dedicated README file](im_connector/im_library/README.md).

### Long-term objective

Eventually, the FastAPI app will be deprecated and replaced by a Kafka consumer. This will provide an interface between the Kafka-based messaging architecture and the IM REST API.

## Build and startup

The code is packaged as a Docker image.

### Building the image

The image can be built with the command:

```
docker build -t <TAG>:<VERSION> -f docker/Dockerfile
```

### Running the container

The IM Connector only relies on a single environment variable:

```
IM_HOST = https://www.example.com:8800
```

This is the URL of the target IM deployment. By default, the IM REST API is exposes at port 8800. If the target deployment has custom settings, change the URL accordingly

The value of this variable can either be set via a `.env` file (use `.env.example` as reference) or via command line parameters.

The image can be started directly with the command:

```
docker run -d -p 8000:80 -e IM_HOST="https://www.example.com:8800" <TAG>:<VERSION>
```

In addition, a `docker-compose.yaml` is also provided. In this case, ensure the image is retrieved from the appropriate repository (or from a local build, if necessary).
