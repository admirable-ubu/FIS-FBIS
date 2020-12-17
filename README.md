# Project FIS PI19/00670
[![made-with-python](https://img.shields.io/badge/Coded%20with-Python-21496b.svg?style=flat-square)](https://www.python.org/)
[![run-on-docker](https://img.shields.io/badge/Runs%20on-Docker-2395ed.svg?style=flat-square)](https://www.python.org/)
![GitHub repo size](https://img.shields.io/github/repo-size/jlgarridol/FIS-FBIS?style=flat-square)
![GitHub](https://img.shields.io/github/license/jlgarridol/FIS-FBIS?style=flat-square) 
![Maintenance](https://img.shields.io/maintenance/yes/2020?style=flat-square)




Repository of the software for the FIS' project PI19/00670: Feasibility and cost-effectiveness study of the use of telemedicine is being developed with a multidisciplinary team for the prevention of falls in Parkinson's disease

## Abstract
During the last decades tele-rehabilitation has been consolidated as a solution for many diseases because of, mainly, its good results, its reduction of costs, and the possibility of reaching remote places. 
In addition, the intrinsic distance of tele-medicine eliminates the exposure of vulnerable patients to unnecessary risks.
One of the problems of tele-rehabilitation is the need of a professional for assessing the proper performance of the exercises, which reduces one of its advantages, that is, the cost cutting.
This paper focuses on a low-cost tele-rehabilitation system for patients that suffer from Parkinson disease in remote villages or inaccessible places.
The paper presents a full-stack, using Big Data frameworks, that makes possible the communication between the patient and the occupational therapist, the recording of the sessions, and seeks the automatic evaluation of the exercises by using Artificial Intelligence techniques.
To ingest the huge amount of videos that simultaneous patients could produce, Big Data technologies were used.
Moreover, the use of deep neural networks makes possible the proper identification of the patients' skeleton which would allow automatic evaluation of the exercises helping to the therapist in his or her tasks.
The system is being currently applied in Spain, more specifically in the province of Burgos, in the framework of a national project for evaluating the use of a multidisciplinary tele-rehabilitation fall prevention program.

## Output examples

<p align="center">
  <img src="https://raw.githubusercontent.com/jlgarridol/TFM-FIS-IF/master/doc/img/gifdemo.gif" width="1000"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Josemi/TFM-FIS-IA/master/doc/Latex/img/josemi.gif" width="1000"/>
</p>

## Deploy

All commands must be executed in folder ```"src/scripts/deploy/"```.

1. **Build docker images**

First it is necessary to build the docker images.

```bash
$ docker build -f ../../dockers/fishubu/base/Dockerfile -t fishubu-base:1.0.0 ../../
$ docker build -f../../dockers/fishubu/enviroment/Dockerfile -t fishubu-env:1.0.0 ../../
$ docker build ../../dockers/spark/base -t spark-base-fis:2.4.5
$ docker build ../../dockers/spark/master -t spark-master-fis:2.4.5
$ docker build ../../dockers/spark/worker -tspark-worker-fis:2.4.5
```

2. **Start the server**

To support the tele-rehabilitation system it is necessary to start the service of Kafka and Spark
   
```
$ ./start-server <output> <n. of cpu for master> <n. of workers > <n. of cpu for workers> <memory per workers>
```

3. **Create a new stream**

For each tele-rehabilitation a new stream has to be created.

```
$ ./new-stream "parameters to emitter.py (keep blank in explotation)" "parameters to consumer.py"
```

This command returns by ```STDOUT``` the identifier of the stream. It is necessary to save it to close the stream.

See *Manual creation* for parameters of ```emitter.py``` and for ```consumer.py```.

4. **Close a stream**

When tele-rehabilitation has finished the stream must be closed to release the machine's resources.

```
$ ./stop-stream ,stream identifier>
```

5. **Close the server**

The server must be securely closed.The following command is used to ensure orderly shutdown.

```
$ ./stop-server
```

### ***Manual creation***

The following python scripts take care of the enqueue and processing of the video stream.

1. ```emitter.py```

Script for sending frames to an UDP server. Necessary for pre-recorded videos.

```
Syntax:
	emitter.py --ip=localhost --port=12345 --file=video.webm
-----------------------------------------------------------
Communication parameters
	--ip=<Ip of UDP broadcast> 
		(Default: localhost)
	--port=<Port of UDP broadcast>
	--file=<Video source>
	
Stream management parameters
    --resize=<Proportion> 
    	(Default: 1.0)
    -f <FPS> | --fps=<FPS> 
    	(Default: 10) frame rate of the video to be broadcast
```
2. ```consumer.py```
   
Script for parallel frame processing.

```
Syntax
	consumer.py --ip=localhost --port=12345 --topic=queue 
-----------------------------------------------------------
Communication parameters
	--output==<Output folder or stream> 
		(Default: output)
	--sparkhost=<Spark host>
		(Default: local)
	--kafkahost=<Kafka host> 
		(Default: localhost:9092)
	--topic=<Kafka topic> 
		(Default: video-stream-event)

Stream management parameters
	-a -> Anonymize faces, by default pixelated
		-g <Factor> | --blur=<Factor>
			(Default: 3) Blur anonymizing
		-p <Factor> | --pixel=<Factor>
			(Default: 15) Pixel anonymizing
	-b -> Auto brightness adjustment
	-c -> Auto contrast adjustment
	-f <FPS> | --fps=<FPS> 
    	(Default: 10) frame rate of the video to be broadcast
	--no-save -> Don't save frames
```


3. ```producer.py```

Script for the frame enqueue in Kafka.

```
Syntax
	producer.py --ip=localhost --port=12345 --topic=queue 
-----------------------------------------------------------
Communication parameters
	--ip=<Ip of UDP broadcast> 
		(Default: localhost)
	--port=<Port of UDP broadcast>
	--kafkahost=<Kafka host> 
		(Default: localhost:9092)
	--topic=<Kafka topic> 
		(Default: video-stream-event)
```

## Third party 
### Apache 2.0:
- **[Apache Kafka](https://kafka.apache.org/)** from *Apache Foundation* 
- **[Apache Zookeeper](https://zookeeper.apache.org/)** from *Apache Foundation* 
- **[Apache Spark](https://spark.apache.org/)** from *Apache Foundation* 
- **[Docker CP](https://github.com/confluentinc/cp-docker-images)** from *Confluentic* 
- **[Jitsi Meet, Jitsi Videobridge and Jibri](https://github.com/jitsi)** from *Jitsi* 
### GPLv3
- **[Clúster Spark Docker](https://github.com/mjuez/spark-cluster-docker)** from *Mario Juez Gil* 
### BSD and variants
- **[Caffe](https://github.com/BVLC/caffe)** from *Berkeley Vision and Learning Center* 
- **[Flask](https://palletsprojects.com/p/flask/)** from *The Pallets Projects* 
- **[Jinja](https://palletsprojects.com/p/jinja/)** from *The Pallets Projects* 
- **[OpenCV](https://opencv.org/)** from *Intel Corporation, Xperience AI* 
- **[Seaborn](https://seaborn.pydata.org/)** from *Michael Waskom* 
### MIT
- **[Bootstrap 4](https://getbootstrap.com/)** from *Twitter* 
- **[jQuery](https://jquery.**com**/)** from *JS Foundation* 

