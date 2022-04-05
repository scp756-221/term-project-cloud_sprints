VER=v1.0
HOST_DIR=$(HWD)/s3

# this is needed to switch M1 Mac to x86 for compatibility with x86 instances/students
ARCH=--platform x86_64

build-s3:
	docker image build $(ARCH) -f Dockerfile --build-arg EXERARG=$(VER) --build-arg ASSIGN=$(ASSIGN) -t s3-v1:$(VER) .

run-s3:
	docker container run $(ARCH) -it --rm -p 30003:30003 -v $(HOST_DIR):/data --name s3 s3-v1:$(VER)