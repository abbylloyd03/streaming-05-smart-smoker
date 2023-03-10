"""
    This program listens for messages from the bbq_producer.py continuously. 
    Messages are changed to floats, and a message is printed if the smoker 
    temp has decreased by more than 15 degree F.

    Author: Abby Lloyd / Denise Case
    Date: February 11, 2023

"""

import pika
import sys
from collections import deque

#####################################################################################

# define variables
bbq_deque = deque(maxlen=5)
queue_name = '01-smoker'
alert_message = "Smoker Alert: Smoker temperature has decreased by more than 15 degrees!"
no_alert_message = "Done."

#####################################################################################

# define a callback function to be called when a message is received
def callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string and store in variable 
    message = body.decode()
    print(f" [x] Received {message}")
    # If message is empty string, change to zero
    if message == '':
        message = 0
    else:
        message = message
    # change message to float and append to deque
    bbq_deque.append(float(message))
    # Add readings to list and disregard any non-readings (0)
    list_of_readings = []
    for item in bbq_deque:
        if item > 0:
            list_of_readings.append(item)
    # If there are more than one reading in list, calculate difference
    if len(list_of_readings) > 1:
        difference = max(list_of_readings) - min(list_of_readings)
    else:
        difference = 0
    # print message if difference is greater than 15 degrees and max is read before min
    if difference > 15 and list_of_readings.index(max(list_of_readings)) < list_of_readings.index(min(list_of_readings)):
        final_alert = alert_message
    else:
        final_alert = no_alert_message
    # when done with task, tell the user
    print(f" [x] {final_alert}")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    #####################################################################################

# define a main function to run the program
def main(hn: str = "localhost", qn: str = "task_queue"):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume( queue=qn, on_message_callback=callback)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()

#####################################################################################

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main("localhost", queue_name)
