# Streaming Event Pipeline with Apache Kafka

This project includes files to create and define a streaming event pipeline around Apache Kafka and its ecosystem which will process data from the [Chicago Transit Authority](https://www.transitchicago.com/data/) to simulate the status of train lines in real time.

## Event Pipeline
This is the structure of the event pipeline developed:
![Project Architecture](https://raw.githubusercontent.com/Gares95/Streaming-Event-Pipeline_Apache-Kafka/master/Img/diagram.png)

**Arrival and Turnstiles** is a kafka **producer** which produces train arrival and turnstiles information into our Kafka cluster.

The program uses **Kafka Connect** to integrate data sources (in this case Postgres) and extract data from our *stations_table* and send it into our Kafka Cluster. It also uses **REST Proxy** to consume and produce data to Kafka using an HTTP client. **Weather** is a python script that acts as an HTTP client and emits weather data to our REST Proxy.

**Transit Status Server** is a kafka **consumer** to consume data from our Kafka topics in our Kafka cluster.  which produces train arrival and turnstiles information into our Kafka cluster. It also uses **Faust** and **KSQL** to extract data and transform it.

## Files

**Producers**
In the producers folder you will find the next files:
- Weather.py: Python Scripts that emits weather data to our REST Proxy.
- Weather.py: Python Scripts that emits weather data to our REST Proxy.
- Weather.py: Python Scripts that emits weather data to our REST Proxy.
- Weather.py: Python Scripts that emits weather data to our REST Proxy.

### Credits
Udacity provided the template and the guidelines to start this project.
The completion of this was made by Guillermo Garcia and the review of the program and the verification that the project followed the proper procedures was also made by my mentor from udacity.