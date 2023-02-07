# streaming-05-smart-smoker
## Abby Lloyd
## 7 Feb 2023

> Create a producer to stream information from a smart smoker. 

## Challenge to Solve
We want to stream information from a smart smoker. Read one value every half minute. (sleep_secs = 30)

smoker-temps.csv has 4 columns:

[0] Time = Date-time stamp for the sensor reading
[1] Channel1 = Smoker Temp --> send to message queue "01-smoker"
[2] Channel2 = Food A Temp --> send to message queue "02-food-A"
[3] Channel3 = Food B Temp --> send to message queue "02-food-B"

## Requirements
- RabbitMQ server running
- pika installed in your active environment

## RabbitMQ Admin
- See http://localhost:15672/Links to an external site.

## General Design Questions
- How many producers processes do you need to read the temperatures: 1
- How many queues do we use: 3
- How many listening callback functions do we need (Hint: one per queue): 3

## Results
- A an example of the producer running in the terminal

![Python terminal](Terminals.png)

