import numpy as np
from ast import literal_eval

def check(particles, sen_arr, sen_poses):
    for j, sen in enumerate(sen_arr):
        if sen[0] == "1":
            pos = sen_poses[j]
            for k, p in enumerate(particles):
                if pos[0]-2.5 < p[1] and pos[0]+2.5 > p[1]:
                    if pos[1]-2.5 < p[2] and pos[1]+2.5 > p[2]:
                        particles[k] = [1/25+p[0]/2, p[1], p[2]]
    normalized_stuff = particles[:,0]/sum(particles[:,0])
    for i, norm in enumerate(normalized_stuff):
        particles[i,0] = norm
    
    print(particles)
    return particles

results = np.array((225,2))
# sen_1_pos = (7.34600019, -5.85099983)
# sen_2_pos = (6.95800018, -2.59299994)
# sen_3_pos = (3.24300003, -11.1639996)
# sen_4_pos = (-2.41499996, -1.18299997)
# sen_5_pos = (3.33800006, 2.35500002)
sen_1_pos = (4.34600019, -5.85099983)
sen_2_pos = (5.55800018, -2.59299994)
sen_3_pos = (3.24300003, -5.1639996)
sen_4_pos = (-2.11499996, -1.78299997)
sen_5_pos = (3.33800006, 3.75500002)

sen_poses = [sen_1_pos, sen_2_pos, sen_3_pos, sen_4_pos, sen_5_pos]

num_particles = 1000
particles = np.zeros((num_particles,3))

currTime = 90

file1 = open('SensorParsed_1.txt', 'r')
Lines_1 = file1.readlines()
file2 = open('SensorParsed_2.txt', 'r')
Lines_2 = file2.readlines()
file3 = open('SensorParsed_3.txt', 'r')
Lines_3 = file3.readlines()
file4 = open('SensorParsed_4.txt', 'r')
Lines_4 = file4.readlines()
file5 = open('SensorParsed_5.txt', 'r')
Lines_5 = file5.readlines()


#instantiate particles
for i in range(num_particles):
    p_x = np.random.uniform(-2, 10)
    p_y = np.random.uniform(-12, 10)
    particles[i, 0] = 1/num_particles
    particles[i, 1] = p_x
    particles[i, 2] = p_y

arr = []
hjkl = 0
for i,line in enumerate(Lines_1):
    sen_1 = Lines_1[i]
    sen_2 = Lines_2[i]
    sen_3 = Lines_3[i]
    sen_4 = Lines_4[i]
    sen_5 = Lines_5[i]

    particles = check(particles, [sen_1, sen_2, sen_3, sen_4, sen_5], sen_poses)
    resampledInds = np.random.choice(range(num_particles), size=200, p=particles[:,0])

    new_particles = np.zeros((num_particles,3))
    for l in range(200):
        new_particles[l] = particles[resampledInds[l]]
    for l in range(800):
        p_x = np.random.uniform(-2, 10)
        p_y = np.random.uniform(-12, 10)
        new_particles[200+l,0] = 0
        new_particles[200+l,1] = p_x
        new_particles[200+l,2] = p_y

    # particles = new_particles
    
    avg_x = 0
    avg_y = 0
    avg_c = 0
    for part in particles:
        if True:
            avg_x += part[1] * part[0]
            avg_y += part[2] * part[0]
            avg_c += part[0]

    arr.append((round(avg_x/avg_c,7), round(avg_y/avg_c,7), hjkl))

    # ind = np.argmax(particles[:,0])
    # arr.append((round(particles[ind][1]+np.random.normal(0,2),7),  round(particles[ind][2]+np.random.normal(0,2), 7), hjkl))
    hjkl += 1


# Using readlines()
file1 = open('characterPos.txt', 'r')
Lines = file1.readlines()

# start 90 and go .4 seconds to 180
# Strips the newline character
list_ = []
currCount = 90
asdf = 0
for line in Lines:
    beg = line.find("pos: ")
    end = line.find(" time:")
    val = literal_eval(line[beg+5:end])
    list_.append([val[0], val[2], asdf])
    asdf += 1

# print(list_)
# print(arr)
list_ = np.array(list_)
arr = np.array(arr)
list_ind = 0

dist_arr = []
for i, coord in enumerate(arr):
    dist_arr.append(np.linalg.norm([coord[0] - list_[int(list_ind),0], coord[1] - list_[int(list_ind),1]]))
    list_ind += .418
print(dist_arr)
print(sum(dist_arr)/len(dist_arr))

import matplotlib.pyplot as plt

plt.rcParams["figure.autolayout"] = True

f, ax = plt.subplots()

points = ax.scatter(list_[:,0], list_[:,1], c=list_[:,2], s=50, cmap="plasma")
f.colorbar(points)

plt.show()

plt.rcParams["figure.autolayout"] = True

f, ax = plt.subplots()

points = ax.scatter(arr[:,0], arr[:,1], c=arr[:,2], s=50, cmap="plasma")
f.colorbar(points)

plt.show()

plt.rcParams["figure.autolayout"] = True

f, ax = plt.subplots()

plt.plot(range(len(dist_arr)), dist_arr)

plt.show()