from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint
from kubernetes.stream import stream

config.load_incluster_config()
api_instance = client.CoreV1Api()

# get current slskd pod name
ret = api_instance.list_namespaced_pod(
    "slskd", watch=False, label_selector="app.kubernetes.io/name=slskd"
)
for item in ret.items:
    print("%s" % (item.metadata.name))
    pod_name = item.metadata.name

update_port_command = [
    "/bin/sh",
    "-c",
    "LISTEN_PORT=$(cat /tmp/gluetun/forwarded_port);sed -i 's/listen_port:.*/listen_port: '\"$LISTEN_PORT\"'/' /app/slskd.yml",
]
try:
    api_response = stream(
        api_instance.connect_get_namespaced_pod_exec,
        pod_name,
        "slskd",
        command=update_port_command,
        container="slskd",
        stderr=True,
        stdin=True,
        stdout=True,
        tty=False,
    )
except ApiException as e:
    print("Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: %s\n" % e)

print("%s" % api_response)
