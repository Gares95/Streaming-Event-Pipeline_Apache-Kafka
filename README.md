# Streaming Event Pipeline with Apache Kafka

This project includes files to create and define a streaming event pipeline around Apache Kafka and its ecosystem which will process data from the [Chicago Transit Authority](https://www.transitchicago.com/data/) **(CTA)** to simulate the status of train lines in real time.

With this repository it will be possible to monitor movements of trains from station to station using your web browser through *http://localhost:8889* (the Transit Status Page).

![Transit Status Page](https://raw.githubusercontent.com/Gares95/Streaming-Event-Pipeline_Apache-Kafka/master/Img/Website-page.png)

## Project Architecture
This is the structure of the event pipeline developed:
![Project Architecture](https://raw.githubusercontent.com/Gares95/Streaming-Event-Pipeline_Apache-Kafka/master/Img/diagram.png)

The structure consists of different ecosystem tools of Kafka (such as a REST Proxy and Kafka Connect), a Kafka Cluster including producers and consumers to create and process data, and different programs to produce other relevant information that the Kafka cluster will consume and process.

### Elements of our Stream Event Pipeline
**Arrival and Turnstiles** is a kafka **producer** which produce train arrival and turnstiles information into our Kafka cluster.

The program uses **Kafka Connect** to integrate data sources (in this case Postgres) and extract data from our *stations_table* and send it into our Kafka Cluster. It also uses **REST Proxy** to consume and produce data to Kafka using an HTTP client. **Weather** is a python script that acts as an HTTP client and emits weather data to our REST Proxy.

**Transit Status Server** is a kafka **consumer** that consumes data from our Kafka topics in our Kafka cluster.
The project also uses **Faust** and **KSQL** to extract data and transform it.

## Files

**Producers**
In the producer folder you will find the next files:

- connector.py: Jdbc source connector that connects to Postgres and extracts data from the *station* table and post it into Kafka.

- simulation.py: Python script to start running the simulation (it also defines train schedules).

- Models:
    - line.py: Constructs all stations and train objects to stations. It also handles their events such as movement of trains between stations and turnstile events.
    - producer.py: Kafka producer that creates topics (if they don't exists) and produces **Train Arrival** and **Turnstiles** data in our kafka cluster. Arrivals indicate that a train has arrived in a particular station and *turnstile events* indicates when a passenger has enter the station. 
    - station.py: It creates topics for each station in Kafka to track the arrival events. The station emits an arrival event to Kafka whenever the Station.run() function is called.
    - train.py: Defines CTA Train Models.
    - turnstile.py: Creates a turnstile data producer.
    - weather.py: Python Script that periodically emits weather data to our REST Proxy.

- Schemas: This folder contains the avro schemas for the different types producer and consumed by the Kafka cluster.


**Consumer**
In the consumer folder you will find the next files:

- consumer.py: Jdbc source connector that connects to Postgres and extracts data from the *station* table and post it into Kafka.

- faust_stream.py: Defines trends calculation for stations. It also defines the records that ingest from Kafka (*Station*) and other that produce before sending it to the Kafka cluster (*TransformedStation*).

- ksql.py: It uses ksql to transform the data stream obtained form the turnstile producer (transforms *turnstile* data to a *turnstile summary*). (it also defines train schedules).

- server.py: Python file to instanciate the different Kafka consumers.

- topic_check.py: Python file to check if topic exists.

- Models:
    - line.py: Contains functionality related to Lines handeling stations and train locations. It also extracts and process data from kafka messages of the topics produced by producers.
    - lines.py: Handle Line's objects and process it messages (depending on the *color* attribute).
    - station.py: Proccess kafka station messages and handles arrivals and departure of trains from stations.
    - weather.py: Handles incoming weather data.


## Prerequisties

To complete the project, the following are required:

- Docker
- Python 3.7
- A minimum of 16gb+ RAM and a 4-core CPU on your computer to execute the simulation

You will also need to install some python modules to use kafka and faust. You can use: `pip install -r requirements.txt` to install these requirements that are located in the  *consumer* and the *producer* folders.

## Running the simulation
**Note: You must allocate at least 4gb RAM to your Docker-Compose environment to run locally**

To run the simulation, you must first start up the Kafka ecosystem on your machine utilizing Docker-Compose.

`%> docker-compose up`

Docker-Compose will take 3-5 minutes to start, depending on your hardware. 

Once Docker-Compose is ready, the following services will be available on your local machine:

![Url services of the enviroment](https://raw.githubusercontent.com/Gares95/Streaming-Event-Pipeline_Apache-Kafka/master/Img/docker-url.png)
Note that to access these services from your own machine, you will always use the `Host URL` column.

When configuring services that run within Docker-Compose, like Kafka Connect, you must use the `Docker URL`. When you configure the **JDBC Source Kafka Connector**, for example, you will want to use the value from the Docker URL column like this:

    curl -X POST -H 'Content-Type: application/json' -d '{
        "name": "stations",
        "config": {
            "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
            "key.converter": "org.apache.kafka.connect.json.JsonConverter",
            "key.converter.schemas.enable": "false",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "value.converter.schemas.enable": "false",
            "batch.max.rows": "500",
            "connection.url": "jdbc:postgresql://localhost:5432/cta",
            "connection.user": "cta_admin",
            "connection.password": "chicago",
            "table.whitelist": "stations",
            "mode": "incrementing",
            "incrementing.column.name": "stop_id",
            "topic.prefix": "org.chicago.cta",
            "poll.interval.ms": "1000"
        }
      }' \
      http://kafka-connect:8083/connectors


## Running the simulation
There are two pieces to the simulation, the producer and consumer. To run the simulation it is critical that you open a terminal window for each piece and run them at the same time. If you do not run both the producer and consumer at the same time you will not be able to successfully run the simulation.

**To run the producer:**
1. `cd producers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python simulation.py`

**To run the Faust Stream Processing Application:**
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `faust -A faust_stream worker -l info`

**To run the KSQL Creation Script:**
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python ksql.py`

**To run the consumer:**
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python server.py`

Once the server is running, you may hit `Ctrl+C` at any time to exit.

### Credits
Udacity provided the template and the guidelines to start this project.
The completion of this was made by Guillermo Garcia and the review of the program and the verification that the project followed the proper procedures was also made by my mentor from udacity.