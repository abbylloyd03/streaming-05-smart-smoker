"""
    This program reads in a csv file and for each row sends 
    three different messages to three different queues on the RabbitMQ server.

    Author: Abby Lloyd / Denise Case
    Date: Feb 7, 2023

"""

import pika
import sys
import webbrowser
import csv
import time

def offer_rabbitmq_admin_site():
    """
    If show_offer is True, offer to open the RabbitMQ Admin website. 
    Otherwise, open automatically.
    """

    show_offer = False
    if show_offer == True:
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """


    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site()
    # Declare a variable to hold the input file name
    input_file_name = "/Users/Abby/Documents/44-671 Streaming Data/Module 5/streaming-05-smart-smoker/smoker-temps.csv"
    # Create a file object for input (r = read access)
    input_file = open(input_file_name, "r")
    # Create a csv reader for a comma delimited file
    reader = csv.reader(input_file, delimiter=",")
    # Declare a variable to hold the amount of sleep time between messages
    sleep_time = 30
    # Then, for each data row in the reader
    for row in reader:
        for (t, ch1, ch2, ch3) in reader:
            # get the message from reader
            # if no arguments are provided, use the default message
            # use the join method to convert the list of arguments into a string
            # join by the space character inside the quotes
            message1 = " ".join(sys.argv[1:]) or f'{ch1}'
            message2 = " ".join(sys.argv[1:]) or f'{ch2}'
            message3 = " ".join(sys.argv[1:]) or f'{ch3}'
            # send the messages to the queue 
            send_message("localhost","01-smoker",message1)
            send_message("localhost","02-food-A",message2)
            send_message("localhost","02-food-B",message3)
            # sleep for the sleep_time indicated above
            time.sleep(sleep_time)
