# slskd-port-forward-gluetun-server
A Python script and Docker container for automatically setting slskd listening port from Gluetun's control server within a Kubernetes cluster

See: https://github.com/slskd/slskd/issues/1011

RBAC permission needed:

```yaml
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: portfwd
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
- apiGroups: [""]
  resources: ["pods/exec"]
  verbs: ["create","get"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: portfwd
subjects:
- kind: ServiceAccount
  name: default
  namespace: slskd
roleRef:
  kind: Role
  name: portfwd
  apiGroup: rbac.authorization.k8s.io
```

Cronjob example:
```yaml
---
apiVersion: v1
items:
- apiVersion: batch/v1
  kind: CronJob
  metadata:
    name: update-portforward
    namespace: slskd
  spec:
    schedule: */5 * * * *
    concurrencyPolicy: Forbid
    jobTemplate:
      spec:
        template:
          spec:
            containers:
            - image: ghcr.io/tieum/slskd-port-forward-gluetun-server:main
              imagePullPolicy: IfNotPresent
              name: update-portforward
```
