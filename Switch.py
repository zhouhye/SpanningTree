# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

# from Message import *
import Message
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.root = self.switchID
        self.distance = 0
        self.switchThrough = self.switchID
        self.activeLinks = set([])

    def send_neighbors_messages(self):
        for neighbor in list(self.links):
            path_through = True if neighbor in self.activeLinks else False
            msg = Message(self.root, self.distance, self.switchID, neighbor, path_through)
            self.send_message(msg)

    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for neighbor in self.links:
            msg = Message(self.root, 0, self.switchID, neighbor, False)
            self.send_message(msg)
        return

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + 1
            self.switchThrough = message.origin
            self.activeLinks.add(self.switchThrough)
            self.send_neighbors_messages()
        elif message.root == self.root:
            if message.distance + 1 < self.distance:
                self.distance = message.distance + 1
                self.switchThrough = message.origin
                self.activeLinks.add(self.switchThrough)
                self.send_neighbors_messages()
            elif message.distance + 1 == self.distance:
                if message.origin < self.switchThrough:
                    self.activeLinks.remove(self.switchThrough)
                    self.switchThrough = message.origin
                    self.activeLinks.add(self.switchThrough)
                    self.send_neighbors_messages()
            else:
                if message.pathThrough:
                    self.activeLinks.add(message.origin)
                ###?
                else:
                    if message.origin in self.activeLinks: ##??
                        self.activeLinks.remove(message.origin)

        return

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        log_list = []
        for active_link in sorted(self.activeLinks):
            log_list.append(f"{self.switchID} - {active_link}")
        log_string = ', '.join(log_list)
        return log_string
