# -*- coding: cp1252 -*-
import sys
import math
from naoqi import ALProxy

def main(robot_ip, robot_port):
    # Initialize connection with NAO robot
    try:
        tts = ALProxy("ALTextToSpeech", robot_ip, robot_port)
        asr = ALProxy("ALSpeechRecognition", robot_ip, robot_port)
        motion = ALProxy("ALMotion", robot_ip, robot_port)
    except Exception as e:
        print("Error connecting to the robot:", e)
        sys.exit(1)

    # Set up questions and responses
    question_responses = {
        "hello": "Hello! How are you?",
        "how are you": "I'm fine, thank you for asking.",
    }

    # Set up the voice recognition vocabulary
    vocabulary = question_responses.keys()
    asr.setVocabulary(vocabulary, False)

    # Define the response function
    def process_response(value):
        if value in question_responses:
            response = question_responses[value]
            tts.say(response)
            if value == "come to me":
                # Move 5 centimeters forward
                motion.move(0.05, 0, 0)
        else:
            tts.say("I'm sorry, I can't answer that question.")

    # Connect the response function to the voice recognition event
    asr.subscribe("Test_ASR")
    asr.signal.connect(process_response)

    # Keep the program running until Ctrl + C is pressed
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    # Unsubscribe and clean up resources before exiting
    asr.unsubscribe("Test_ASR")

if __name__ == "__main__":
    robot_ip = "192.168.1.100"  # Replace with the IP address of your NAO robot
    robot_port = 9559

    main(robot_ip, robot_port)
