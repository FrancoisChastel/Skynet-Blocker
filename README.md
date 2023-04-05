# Skynet Blocker's

Repository holding services in charge of Anonimisation related works. For the moment CSV and Sydonia are holds there.

## Table of contents

- [Skynet Blocker's](#skynet-blockers)
  - [Table of contents](#table-of-contents)
  - [Technologies](#technologies)
  - [API's definition](#apis-definition)
  - [Contributing](#contributing)
  - [Building targets](#building-targets)
  - [Deploying](#deploying)
  - [Security](#security)
  - [Clients](#clients)
  - [Production context](#production-context)
  - [Authors](#authors)

## Technologies

This project rely on the following technologies :

- Golang v1.90.0 ;
- Python v3.10.0 ;
- gRPC v1.49.0 ;
- Protobuf v3 ;
- Docker v20 ;
- Kubernetes apiV1 ;
- Bazel v5.3.1.

## API's definition

We recommend using Swagger's UI with the file `clients/web/skynet.swagger.json` for more information over the different objects. Otherwise the protos file are defined here `protos/skynet.pro`

## Contributing

To run the project please install bazel, python and golang as the toolchains for the builds are required for it to run the full project (doocker may be needeed as well in case you want to publish it). The recommended tool for interacting with gRPC-service on mac is BloomRPC in our context.

For bazel please use Bazelisk as it will allow you to catch up with the right versionning of our used toolchain for build purpose.

Here are the command to install the project prerequisities:

```bash
brew install bazelisk
```

Please install [GoLang](https://go.dev/doc/install). If you are on mac you may have to have your xCode dev's env properly installed if this is not the case please run :

```bash
xcode-select --install
```

Once all of this done and if you are familliar with previously mentionned project you are good to go.

## Building targets

Each directory holding a `BUILD.bazel` has targets which are usable for the sake of simplicty here are the main ones :

If you are on mac, there is a bug in `libomp` lib (lol), please see the following thread for more info : https://github.com/microsoft/LightGBM/issues/4229#issuecomment-930614380 

- gRPC's service :

```bash
make run
```

- Gateway's service :

```bash
make gateway
```

- Re-Generate Swagger's doc and Re-Generate Python gRPC's client :

```bash
make update-protos
```


## Deploying

Depending on the target you aim and the platform you are targeting the steps can be slightly different, as we target linux x86 architecture the easiest way is to run a docker image to build our image.
For that purpose please follow these instructions

```bash
make launch 
```

This should have launched you a docker container, you should accecss to his terminal and run the following commands

```bash
make docker-install
```

Then, we will login to the registry (update the secret key inside you makefile)

```bash
make publish 
```

## Security

We now have one-shot token usage, please had as an header with the key `x-api-key`, it will be needed for both `json+HTTP/1` and `gRPC+HTTP/2` calls. To configure it please update the `apiKey` inside the codebase.

## Clients

You have both web (swagger doc can generate clients) and Python gRPC clients ready to use in the directory `clients/`

- Python's client:

Install grpc and grpc-tools

```bash
python -m pip install grpcio
python -m pip install grpcio-tools
```

Inside your code you will have client generated that can be used with some conf after having properly importing both gRPC client `clients/python/skynet_pb2_grpc.py` and the protobuf file `clients/python/skynet_pb2.py`.

You can use autocompletion to list all the available services, but there are the same as the ones available on HTTP/1, the documentation generated for Swagger is then valid for this as well.

```python
def run():
    with grpc.insecure_channel('localhost:50052') as channel: #Please change the channel to secure and the right URI
        stub = skynet_pb2_grpc.SkynetBlockerStub(channel)
        response = stub.Visualizer(skynet_pb2.VisualizerRequest(...))
        print("Visualization :" + response.message)
```

## Production context

The API's are running in these context :

- 1.0.0-beta : `skynet-blocker.datafid.sudoers.fr`

All the docs of the HTTP API's are holds by the postman and kept updated. For the gRPC's SDK, as it contains all the comments and types included there are no need for further explanation

## Authors

- François Chastel - francoi@chastel.co
