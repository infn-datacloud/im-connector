import requests

def create_k8s_deployment(im_url, jwt, tosca_template):
    im_jwt = ""

    k8s_jwt = ""
    k8s_host = ""

    header_list = [
        f"type = InfrastructureManager; token = {im_jwt}",
        f"id = k8sMilano; type = 'Kubernetes'; host = {k8s_host}; token = {k8s_jwt}"
    ]

    headers = {
        "Content-Type": "text/yaml",
        "Authorization": "\\n".join(header_list)
    }

    response = requests.post(im_url, data=tosca_template, headers=headers)
