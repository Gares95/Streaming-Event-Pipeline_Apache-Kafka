"""Defines trends calculations for stations"""
import logging

import faust


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# TODO: Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")
# TODO: Define the input Kafka Topic. Hint: What topic did Kafka Connect output to?
topic = app.topic("com.udacity.stations", value_type=Station)
# TODO: Define the output Kafka Topic
out_topic = app.topic("com.udacity.output", partitions=1)
# TODO: Define a Faust Table
table = app.Table(
    "stations_table.v1",
    default=str,
    partitions=1,
    changelog_topic=out_topic,
)

# Auxiliar function to detect line
def detect_line(Station):
    if(Station.red):
        line = 'red'
    elif(Station.blue):
        line = 'red'
    elif(Station.green):
        line = 'green'
    return line
     

@app.agent(topic)
async def stationsEvent(stream):
    async for st in stream:
        line = detect_line(st)
        tfs = TransformedStation(st.station_id, st.station_name,st.order,line)
        table[st.station_id] = tfs
        

if __name__ == "__main__":
    app.main()
