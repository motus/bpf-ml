def parser(file):
	file1 = open(file, 'r') 
	Lines = file1.readlines() 
	  
	count = 0
	# Strips the newline character 
	i=0
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
						packet.append(byte.strip())
	return final_data

# data = parser("wget")
data = parser("nmap")
print(data)