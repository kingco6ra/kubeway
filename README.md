# kubectl-forwarder

## Overview

Kubectl-Forwarder is a tool designed to automate and simplify the process of port forwarding for services running in
Kubernetes. It allows local access to services operating within a Kubernetes cluster through dynamically allocated ports
on the local machine. The project includes integration with HAProxy for configuring a proxy server to route requests to
services.

## Features

- **Dynamic Port Forwarding**: Automatically identifies and forwards ports for Kubernetes services.
- **HAProxy Configuration Generation**: Automatically generates a configuration file for HAProxy based on current port
  forwardings.
- **Support for gRPC and HTTP**: Supports forwarding for services operating over gRPC and HTTP protocols.

## Quick Start Guide

This quick start guide will walk you through the setup process of the Kubectl-Forwarder tool, from configuring your
services to running the tool using Docker Compose. This will enable you to access your Kubernetes services locally over
specified ports.

### Step 1: Configure your services in `config.yaml`

Before starting, you need to specify the names of your services, the required ports, and the Kubernetes namespace in
the `config.yaml` file. This file dictates how the Kubectl-Forwarder will interact with your Kubernetes services.

Example `config.yaml`:

```yaml
SERVICES:
  - name: service-1
    namespaces:
      - namespace-1
    forwardings:
      - protocol: http
        remote_port: 8080
        
  - name: service-2
    namespaces:
      - namespace-1
      - namespace-2
    forwardings:
      - protocol: grpc
        remote_port: 50051
        # local_port: 50052  if you want set specific port for forwarding.
```

Replace `your-namespace`, `example-service-1`, and `example-service-2` with your actual Kubernetes namespace and service
names. Adjust the port numbers according to your services' configurations.

### Step 2: Run docker-compose

With your config.yaml ready, you can now start the Kubectl-Forwarder using docker-compose. This step assumes you have a
docker-compose.yml file set up for the Kubectl-Forwarder service.
Start the services by running:

```bash
docker-compose up --build
```

### Step 3: Access your services locally

After the Docker Compose process is up and running, your Kubernetes services will be accessible locally through the
dynamically allocated ports. You can access your services using the following URLs:

* **For gRPC services**: `localhost:80/namespace-1/service-2/grpc` and `localhost:80/namespace-2/service-2/grpc`
* **For HTTP services**: `localhost/namespace-1/service-2/http`

Replace **service names** with the actual name of your service. The port `80` might differ based on your Docker Compose and
HAProxy configuration.

## Troubleshooting

If you encounter any issues during the setup, ensure that:

Your KUBECONFIG environment variable in docker-compose.yml correctly points to your Kubernetes config file.
The config.yaml file accurately reflects your Kubernetes services and namespace.
Docker and Docker Compose are correctly installed and updated to their latest versions.
For more detailed troubleshooting, consult the logs of the Docker containers or the output of the Kubectl-Forwarder
script.

## Additional Resources

* [Kubernetes Documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
* [HAProxy Documentation](https://www.haproxy.com/documentation/haproxy-configuration-manual/latest)

For any dependencies or related projects, ensure you refer to their respective documentation or GitHub repositories for
additional setup or configuration instructions.

## Conclusion

With Kubectl-Forwarder, you gain a powerful tool that simplifies the process of developing and testing applications
within Kubernetes by providing easy access to your services. Whether you're debugging a local application or integrating
multiple services, Kubectl-Forwarder streamlines your workflow.

