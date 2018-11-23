import os

result_list = []
child_list = []

def getFileName(path):
	pathString = path.rstrip()
	files = os.listdir(pathString)
	new_list = []
	for file in files:
		child_path = pathString + "/" + file
		# print(child_path)
		if os.path.isdir(child_path) :
			# print(child_path)
			result_list.append(child_path)
			getFileName(child_path)


def getChildFile(path_list):
	for path in path_list:
		pathString = path.rstrip()
		files = os.listdir(pathString)
		for file in files :
			child_path = pathString + "/" + file
			if os.path.splitext(file)[-1] == ".m" or os.path.splitext(file)[-1] == ".h" :
				child_list.append(child_path)
				# print(child_path)


def getFileLineNumber(path_list):
	total_number = 0
	for path in path_list :
		with open(path) as file_object:
			count = len(file_object.readlines())
		# count = len(open(path,'r').readlines())
			total_number += count
	return total_number

if __name__ == '__main__':
	# path1 = input('path :')
	path1 = raw_input('path : ')
	getFileName(path1)
	# print(result_list)
	getChildFile(result_list)
	# print(child_list)
	child_list_number = str(len(child_list))
	# print("total files (.m and .h) : " + child_list_number)
	# print("total lines : " + str(getFileLineNumber(child_list)))
	print "total files (.m and .h) : " + child_list_number
	print "total lines : " + str(getFileLineNumber(child_list))
