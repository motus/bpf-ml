#!/usr/bin/env python3

import pickle


def parser(file):
	file1 = open(file, 'r') 
	Lines = file1.readlines() 
	  
	# Strips the newline character 
	i = 0
	final_data = []
	packet = []
	for line in Lines: 
		i+=1
		if i>2:
			if(line.strip()==''):
				final_data.append(packet)
				packet = []
				i=0
			else:
				arr = line.split("/*")
				byte_data = (arr[0].strip()).split(",")
				for byte in byte_data:
					if(len(byte.strip())>2 and (byte.strip())[0:2]=='0x'):
						packet.append(int(byte.strip()[2:], 16))
	return final_data


for fname in ["nmap", "wget"]:
	data = parser("data/tcp/" + fname)
	print("%s data has %d packets" % (fname, len(data)))
	with open("data/%s.pk" % fname, "wb") as pkfile:
		pickle.dump(data, pkfile)
