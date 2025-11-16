# InfrastructureManager client library in Python

## Introduction
The IM Client library in Python is based on the available documentation:

- IM REST API: https://app.swaggerhub.com/apis-docs/grycap/InfrastructureManager/1.19.0
- IM Authorization file: https://imdocs.readthedocs.io/en/latest/client.html#auth-file

and on the corresponding Java implementation:

- Infrastructure Manager Java API: https://github.com/indigo-dc/im-java-api

This library comprises two components:

- IM Adapter: an automated testing middleware serving the specific purpose of intercepting and parsing the JAVA Orchestrator output directed to the InfrastructureManager. The output of the IM Adapter is directly fed to the IM Client library.
- IM Client: capable of invoking the IM REST API, the IM Client is a high-level object-oriented wrapper of all the available IM endpoints, complemented with an object-oriented representation of the authorization credentials.

## IM Adapter

The Adapter receives a FastAPI Request object, together with its body (when present). The adapter's code does not support any async/await operations, therefore the request body must be deserialized before creating an Adapter instance.

The Adapter can only parse requests meant for the IM REST API. These are received from the JAVA Orchestrator component.

The Adapter identifies:

- the provided credentials and creates the corresponding objects;
- the request type, based on the HTTP method used for the request and the invoked URL;
- the parameters, either path or query parameters, used to compile the request;
- the request HTTP headers.

The Adapter's output consists of two properties:

- `request`, containing the request object;
- `header`, providing a composer class to serialize the request header.

## IM Client

The actual IM Client consists of a single class method called `IMClient.request()`. This method is a wrapper to a `requests.request` call and accepts am `IMBaseRequest` and an `IMHeaderComposer` instances as input. These base objects contain all the information to submit the request to the actual IM.

The `IMClient.request()` method returns the IM response.

### Request types

All requests are represented by objects inheriting from `IMBaseReuqest`. This abstract class defines:

- the HTTP method;
- the endpoint URL;
- the query parameters;
- the request body.

Requests are grouped by HTTP method. Five partial classes are defined: `Get`, `Post`, `Put`, `Patch` and `Delete`.

Actual requests inherit from one of these partial classes.

Thorough type hints guide the user in the object creation process.

### Credential header components

Similarly to the request types, authorization credentials are represented by the `IMCredentialComponentBase` class, which provides a common interface to manipulate request headers.

For each cloud provider, a concrete credential component is defined.

### Usage example

A sample script to submit a request to the IM client (without the IM Adapter middleware) is presented below:

```
from im_library.client.im_client import IMClient
from im_library.client.im_requests.create_infrastructure import CreateInfrastructure, \
    CreateInfrastructureQueryParameters
from im_library.entities.im_base_requests import IMBaseRequest
from im_library.header.credential_components.infrastructure_manager_credential import \
    InfrastructureManagerCredentialComponent
from im_library.header.credential_components.kubernetes_credential import KubernetesCredentialComponent
from im_library.header.im_header_composer import IMHeaderComposer

tosca_file = "<left empty for readability>"

req_qp = CreateInfrastructureQueryParameters(dry_run="true")
req = CreateInfrastructure(body=tosca_file, query_parameters=req_qp)

im_cred = InfrastructureManagerCredentialComponent(token="<some JWT>")
k8s_cred = KubernetesCredentialComponent(host="https://www.example:6443", token="<ome JWT>")

head = IMHeaderComposer()
head.add_credential(im_cred)
head.add_credential(k8s_cred)


response = IMClient.request(request=req, header=head)
```