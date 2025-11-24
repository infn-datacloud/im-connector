# IM Credentials

For each target cloud provider, an object inheriting from IMCredentialComponentbase must be defined.
The constructor must accept all the supported parameters and must take into account default and optional values.

The InfrastructureManagerCredentialComponent is mandatory for all requests to the IM, as it allows the user to authenticate with the IM itself.

