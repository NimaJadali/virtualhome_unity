import numpy as np
from ast import literal_eval

num_sensors = 32
start_time = 113.1909
end_time = 215.1909

# size of the array is a length of sensor readings that matches with charcter pos times
return_array = np.zeros((32,int(end_time - start_time) * 5 + 1))

# For each sensor, convert the readings into 1's and 0's for the numpy array
for i in range(32):
    try:
        file1 = open('SensorsRun_0/sensor_'+ str(i) +'.txt', 'r')
    except:
        continue
    Lines = file1.readlines()

    k = 0

    for j in range(int(end_time - start_time) * 5 + 1):
        line = Lines[k]
        beg = line.find("time: ")
        end = line.find(" moved: ")
        sen_time = literal_eval(line[beg+6:end])
        if (sen_time == start_time + j*.2):
            if (k < len(Lines) - 1):
                k += 1
            return_array[i,j] = 1
        else:
            return_array[i,j] = 0
# Save the numpy array
np.save('sensor_array_0.npy', return_array)