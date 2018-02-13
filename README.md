# IAM Waiter

This is a simple Docker image that will wait for an AWS IAM role to be assigned to it. 

## Purpose

When using [kube2iam](https://github.com/jtblin/kube2iam) along with the [Kubernetes Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler), you may notice the pods expecting a certain IAM role on a new node are starting before kube2iam is ready on that node. That can result in annoying error states every time a new node comes online. This image can be used as an [init container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) to wait for an IAM role to properly be assigned to the pod before the primary container(s) start up. 

## Usage

This is primarily intended to be used as a Kubernetes init container. Here's what a sample pod might look like:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: iam-waiter-test
  namespace: iam-waiter-testing
  annotations:
    iam.amazonaws.com/role: arn:aws:iam::123456789:role/iam-waiter-test
spec:
  initContainers:
  - name: iam-waiter
    image: docker.io/reactiveops/iam-waiter:0.1.0
    env:
      - name: MATCH_ROLE
        value: iam-waiter-test
  containers:
  - name: aws-cli
    image: docker.io/mesosphere/aws-cli:1.14.5
    command: ['watch', '-n', '15', 'aws', 'sts', 'get-caller-identity']
```

IAM Waiter will wait until the pod is given a role that includes the value of the `MATCH_ROLE` environment variable. In this example it will wait for the ARN of the role to include `iam-waiter-test`. Of course the `aws-cli` container in this example would be replaced with whatever container actually needed the IAM role that IAM waiter is waiting for. In this case having the AWS CLI on hand just simplifies this demonstration.


## Configuration

IAM Waiter accepts three environment variables for configuration:

* `MATCH_ROLE` is the only required variable - IAM waiter will wait for the pod's IAM role ARM to include this string.
* `INTERVAL_IN_SECONDS` Will check current IAM role on this interval, defaults to 10 seconds.
* `MAX_ATTEMPTS` Will check IAM role this many times before giving up, defaults to 100.

## License
MIT