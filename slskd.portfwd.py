from __future__ import print_function
import os, time
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config
from pprint import pprint
from kubernetes.stream import stream


def get_current_namespace():
    ns_path = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
    if os.path.exists(ns_path):
        with open(ns_path) as f:
            return f.read().strip()


config.load_incluster_config()
api_instance = client.CoreV1Api()

namespace = get_current_namespace()

# get current slskd pod name
ret = api_instance.list_namespaced_pod(
    namespace, watch=False, label_selector="app.kubernetes.io/name=slskd"
)
for item in ret.items:
    print(
        "found pod %s running in namespace %s"
        % (item.metadata.name, item.metadata.namespace)
    )
    pod_name = item.metadata.name
update_port_command = [
    "/bin/sh",
    "-c",
    "LISTEN_PORT=$(cat /tmp/gluetun/forwarded_port) \
  && sed -i 's/listen_port:.*/listen_port: '\"$LISTEN_PORT\"'/' /app/slskd.yml \
  && IP=$(wget -q -O - ifconfig.co) \
  && echo ip/port: $IP $LISTEN_PORT",
]
try:
    api_response = stream(
        api_instance.connect_get_namespaced_pod_exec,
        pod_name,
        namespace,
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
