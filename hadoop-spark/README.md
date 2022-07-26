# use to create a docker container with pseudo-distributed mode 
# this version uses openjdk:8 official base image based on debian rather than installing openjdk from scratch as in the _pseudo-dist_ directory which is based on ubuntu

## build
1. clone the repo 
2. browse to `containers/pseudo-dist-deb` directory
3. build the docker image (e.g. `# docker build -t hadoop-psdist-deb .`)
4. start a container (e.g. `# docker container run -it --name "hadoopc" -h hadoopc hadoop-psdist`)

## validate
- to make sure the build was successful run `# jps` inside the container. the output should be the hadoop services running like below:
```
<pid> NodeManager
<pid> SecondaryNameNode
<pid> Jps
<pid> NameNode
<pid> ResourceManager
<pid> DataNode
```
- the order of the listing above doesn't matter as long as all 5 hadoop services are running

## notes
- the hadoop ports are not exposed by default.
- you can either edit the `Dockerfile` to `EXPOSE` the required ports, or the container's ip address to use the hadoop services from outside the container
- another option is to use another container that would automatically register the container's hostname as an alias in the docker host's `/etc/hosts` file 
 in order to be able to access the container by name from the docker host

## use hoster service
1. pull the docker-hoster image from my repo on docker hub  
`docker run -d -v /var/run/docker.sock:/tmp/docker.sock -v /etc/hosts:/tmp/hosts asami76/docker-hoster`
3. build and run the pseudo-dist container from the build steps above
4. from the docker host open your browser and type the following in the url `http://hadoopc:9870`
