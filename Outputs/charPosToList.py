from ast import literal_eval

file1 = open('characterPos.txt', 'r')
Lines = file1.readlines()

# start 90 and go .4 seconds to 180
# Strips the newline character
list_ = []
currCount = 90
for line in Lines:
    beg = line.find("pos: ")
    end = line.find(" time:")
    val = literal_eval(line[beg+5:end])
    list_.append(val)

print(list_)