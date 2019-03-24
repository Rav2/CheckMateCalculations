import sys

name = "QqN1_atlas_1712_02332_[" 
start = 0
end = 1191

for ii in range(start, end+1):
	path = name + str(ii) +'].txt'
	file = open(path, 'r')
	data = file.read()
	file.close()
	data=data.replace('/cards', "")
	file = open(path, 'w')
	file.write(data)
	file.close() 
print(data)