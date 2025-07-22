import dataclasses

import requests

from config import get_settings

settings = get_settings()

def create_k8s_deployment(im_url, jwt, tosca_template):
    im_jwt = ""

    k8s_jwt = ""
    k8s_host = ""

    headers = {
        "Content-Type": "text/yaml",
        "Authorization": f"type = InfrastructureManager; token = {im_jwt}\nid = k8sMilano; type = 'Kubernetes'; host = {k8s_host}; token = {k8s_jwt}"
    }

    response = requests.post(im_url, data=tosca_template, headers=headers)

