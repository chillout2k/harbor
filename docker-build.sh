#!/bin/sh

DOCKER_TAG=devel
BASEOS=alpine

docker build --network host -t harbor/${BASEOS}:${DOCKER_TAG} -f docker/${BASEOS}/Dockerfile .
