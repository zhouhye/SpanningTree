# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# Defines a Topology, which is a collection of switches and links between them. Students should not
# modify this file.  This is NOT a topology like the ones defined in Mininet projects.
#
# Copyright 2016 Michael Brown
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Switch import *


class Topology(object):

    def __init__(self, conf_file):
        """Initializes the topology."""
        self.switches = {}
        self.messages = []

        """ This creates all the switches in the Topology from the configuration
            file passed into __init__(). Can throw an exception if there is a
            problem with the config file. """

        try:
            conf = __import__(conf_file)
            for key in list(conf.topo.keys()):
                new_switch = Switch(key, self, conf.topo[key])
                self.switches[key] = new_switch

            # Verify the topology read from file is correct.
            for key in list(self.switches.keys()):
                self.switches[key].verify_neighbors()

        except Exception:
            print(("error importing conf_file " + conf_file))
            raise

    def send_message(self, message):
        if not message.verify_message():
            print("Message is not properly formatted.")
            return

        if message.destination in self.switches[message.origin].links:
            self.messages.append(message)
        else:
            print("Messages can only be sent to immediate neighbors")

    def run_spanning_tree(self):
        # This function drives the simulation of a Spanning Tree.  It first sends the initial 
        # messages from each node by invoking send_intial_message.  Afterward, each message 
        # is delivered to the destination switch, where process_message is invoked.

        for switch in self.switches:
            self.switches[switch].send_initial_messages()
        while len(self.messages) > 0:
            msg = self.messages.pop(0)
            # print(msg.__dict__)
            self.switches[msg.destination].process_message(msg)
        # print('##################################')
        # for s in self.switches:
        #     print(self.switches[s].__dict__)

    def log_spanning_tree(self, filename):
        # This function drives the logging of the text file representing the spanning tree.  
        # It is invoked at the end of the simulation, and iterates through the switches in 
        # increasing order of ID and invokes the generate_logstring function.  That string 
        # is written to the file as provided by the student code.
        with open(filename, 'w') as out:
            for switch in sorted(self.switches.keys()):
                entry = self.switches[switch].generate_logstring()
                entry += "\n"
                out.write(entry)
            out.close()
