/*
* Copyright 2022 Fluximmo all right reserved.
 */
package main

import (
	"flag"

	gateway "github.com/FrancoisChastel/Skynet-Blocker/gatewayutils"
	Skynet_Blocker "github.com/FrancoisChastel/Skynet-Blocker/protos"
	"github.com/golang/glog"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"

	"golang.org/x/net/context"
)

var (
	endpoint   = flag.String("endpoint", "localhost:443", "endpoint of the Elastimmo gRPC service")
	network    = flag.String("network", "tcp", `one of "tcp" or "unix". Must be consistent to -endpoint`)
	swaggerDir = flag.String("swagger_dir", "clients/web", "path to the directory which contains swagger definitions")
)

func main() {
	flag.Parse()
	defer glog.Flush()

	ctx := context.Background()
	opts := gateway.Options{
		Addr: ":80",
		GRPCServer: gateway.Endpoint{
			Network: *network,
			Addr:    *endpoint,
		},
		Mux:        []runtime.ServeMuxOption{runtime.WithIncomingHeaderMatcher(gateway.HeaderMatcher)},
		SwaggerDir: *swaggerDir,
		Services:   gateway.ServiceDefinition{Skynet_Blocker.RegisterSkynetBlockerHandler},
	}
	if err := gateway.Run(ctx, opts); err != nil {
		glog.Fatal(err)
	}
}
