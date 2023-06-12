# use to create a docker container with Spark 3.3.0 and Hadoop 3.3.3 pseudo-distributed mode.
# this version uses openjdk:11 official base image on Debian

## build
1. clone the repo 
2. browse to `spark330_hadoop333` directory
3. build the docker image (e.g. `# docker build -t spark-hadoop .`)
4. start a container (e.g. `# docker container run -it --name "sparkc" -h sparkc spark-hadoop`)

## asami76/spark-hadoop image
Alternatively you can download this image from my Docker Hub account without needing to build it by the running:  
```
docker run -it --rm --name sparkc -h sparkc -v `pwd`/data:/data asami76/spark-hadoop:latest
```

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

- To validate that spark is running run `# ./spark/bin/pyspark` to launch PySpark Shell (Spark is installed in `/usr/local/spark` folder)  
- After the shell is launched, from Docker host open the browser and browse to `http://sparkc:4040` to launch the `Spark UI` page (before that you have to expose the 4040 port or run the hosterr service below).  
- the order of the listing above doesn't matter as long as all 5 hadoop services are running

## notes
- the hadoop and spark ports are not exposed by default.
- you can either edit the `Dockerfile` to `EXPOSE` the required ports, or the container's ip address to use the hadoop services from outside the container
- another option is to use another container that would automatically register the container's hostname as an alias in the docker host's `/etc/hosts` file 
 in order to be able to access the container by name from the docker host

## use hoster service
1. pull the docker-hoster image from my repo on docker hub  
`docker run -d -v /var/run/docker.sock:/tmp/docker.sock -v /etc/hosts:/tmp/hosts asami76/docker-hoster`
2. build and run the spark-hadoop container from the build steps above
3. from the docker host open your browser and type the following in the url `http://sparkc:9870`

## use jupyter notebook to connect to spark
to be able to use Jupyter Notebook to connect to the Spark standalone cluster in the container rather than using the pyspark shell run the following:  
`jupyter-lab --no-browser --allow-root --ip 0.0.0.0 /data/`  
Then copy the provided link to open Jupyter Notebook from the Docker host's browser

