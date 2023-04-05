UNAME := $(shell uname -s)

ifeq ($(UNAME),Darwin) # Mac OS X - see there : https://github.com/microsoft/LightGBM/issues/4229#issuecomment-930614380
  export LIBOMP_USE_HIDDEN_HELPER_TASK=0
  export LIBOMP_NUM_HIDDEN_HELPER_THREADS=0
endif

update-protos: 
	bazel build //protos:all
	yes | cp -i bazel-out/darwin-fastbuild/bin/protos/api_gateway_grpc/protos/*.go protos/
	yes | cp -i bazel-out/darwin-fastbuild/bin/protos/*.py src/protos/
	yes | cp -i bazel-out/darwin-fastbuild/bin/protos/*.pyi src/protos/
	yes | cp -i bazel-out/darwin-fastbuild/bin/protos/swagger_api_gateway_grpc/protos/*.json clients/web/
	yes | cp -i bazel-out/darwin-fastbuild/bin/protos/*.py clients/python/
	yes | cp -i bazel-out/darwin-fastbuild/bin/protos/*.pyi clients/python/
	yes | cp -i bazel-out/darwin-fastbuild/bin/protos/*.go clients/go/
	
update-requirements: 
	pip3 freeze > requirements.txt
	bazel run //:requirements.update

run: 
	bazel run //src:anonimisation

gateway:
	bazel run //cmd/gateway:main


publish:
	bazel run //deployments:docker_push --platforms=@io_bazel_rules_go//go/toolchain:linux_amd64 
	bazel run //deployments:docker_push_gateway --platforms=@io_bazel_rules_go//go/toolchain:linux_amd64 

launch:
	docker run -v /Users/darkraven/Dev/go/src/github.com/FrancoisChastel/Skynet-Blocker:/bazel -u 0 --interactive --entrypoint=/bin/bash gcr.io/bazel-public/bazel:latest 

registry-login:
	docker login --username francoischastel --password dckr_pat__B-u4kTAP6JQcNe2Pcr75Lw40_M

docker-install:
	apt-get install \
			ca-certificates \
			curl \
			gnupg \
			lsb-release
	mkdir -p /etc/apt/keyrings
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
	chmod a+r /etc/apt/keyrings/docker.gpg
	apt-get update
	apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin