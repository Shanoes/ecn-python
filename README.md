# ecn-python
Python lang test for ECN module


Build with:
docker buildx create --name ecnbuilder
docker buildx use ecnbuilder
docker buildx inspect --bootstrap
docker buildx build --platform linux/amd64,linux/arm/v7 -t shanoes/ecn-python:latest --push .


Connect instructions:
add your container to the network ecn_mx80_network
then use opc.tcp://mx80_ua:4840
where mx80_ua is a dns that gives the IP address of the UA container

Run with:
docker run <container id> <OPC_URI> [TAG1] [TAG2]...
e.g. docker run ecnpython opc.tcp://192.168.1.200:4840 TANK1_LEVEL TANK2_LEVEL

The container will create a subscription and read values for 60 seconds then quit. 