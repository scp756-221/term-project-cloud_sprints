# Makefile for standalone Music service (S2)

VER=v1.0

$(eval S2_SERVER=$(shell docker inspect s2 --format '{{.NetworkSettings.IPAddress}}'))
ifeq ("$(S2_SERVER)","")
	S2_SERVER="0.0.0.0"
endif

$(eval S3_SERVER=$(shell docker inspect s3 --format '{{.NetworkSettings.IPAddress}}'))
ifeq ("$(S3_SERVER)","")
	S3_SERVER="0.0.0.0"
endif

S2_PORT=30001

S3_PORT=30003

build-mcli:
	docker image build -f Dockerfile -t mcli:$(VER) .

run-mcli:
	docker container run -it --rm --name mcli mcli:$(VER) python3 mcli.py $(S2_SERVER) $(S3_SERVER) $(S2_PORT) $(S3_PORT)

