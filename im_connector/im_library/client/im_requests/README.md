# Objects representing all the operations supported by the Infrastructure Manager

Each python file contains the definition of an object representing the actual request.
Along with the request object, the query and path parameters supported by each request are also defined in the file.

Example:

The `create_infrastructure.py` file contains the definition of two objects: `CreateInfrastructure` and `CreateInfrastructureQueryParameters`.
The first object represents the IM functionality as a well-formed object and the second class is a dataclass representing the optional query parameters supported by the create infrastructure functionality.

All concrete request classes inherit from five intermediate classes defining each the HTTP verb to be used for the request.
Ultimately, all concrete request classes inherit from the abstract interface `IMBaseRequest`.

Similarly, all query parameters classes inherit from `IMQueryParametersBase`, which in turn inherits from `IMParametersBase`.
Also, all path parameter classes inherit from `IMPathParametersBase`, which in turn inherits from `IMParametersBase`.

The `IMParametersBase` base class is a wrapper around Python's built-in dict. This allows to guide the dict creation while retaining the possibility to serialize the data to a JSON for actual HTTP requests. 