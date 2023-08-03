import numpy as np
from ast import literal_eval

import matplotlib.pyplot as plt

# Setting the constraints of the environment
# Room 1
xmin = -6
xmax = -1.3
ymin = .24
ymax = 4.5
area = (xmax-xmin)*(ymax-ymin)
num_particles = int(50 * area)
x = np.random.uniform(xmin, xmax, size=(num_particles,))
y = np.random.uniform(ymin, ymax, size=(num_particles,))

# Room 2
xmin = -1.3
xmax = 3.9
ymin = -2.1
ymax = 2.4
area = (xmax-xmin)*(ymax-ymin)
num_particles = int(50 * area)
xarr = np.random.uniform(xmin, xmax, size=(num_particles,))
yarr = np.random.uniform(ymin, ymax, size=(num_particles,))

x = np.concatenate((x,xarr))
y = np.concatenate((y,yarr))

# Room 3
xmin = -1.3
xmax = 6.1
ymin = 2.4
ymax = 7.1
area = (xmax-xmin)*(ymax-ymin)
num_particles = int(50 * area)
xarr = np.random.uniform(xmin, xmax, size=(num_particles,))
yarr = np.random.uniform(ymin, ymax, size=(num_particles,))

x = np.concatenate((x,xarr))
y = np.concatenate((y,yarr))


# Room 4
xmin = 6.1
xmax = 11.2
ymin = .24
ymax = 4.91
area = (xmax-xmin)*(ymax-ymin)
num_particles = int(50 * area)
xarr = np.random.uniform(xmin, xmax, size=(num_particles,))
yarr = np.random.uniform(ymin, ymax, size=(num_particles,))

x = np.concatenate((x,xarr))
y = np.concatenate((y,yarr))

f, ax = plt.subplots()
ax.set_xlim(-7.5,12)
ax.set_ylim(-2.5,7.5)

# Instantiate Particles
random_particles = np.zeros((len(x),3))
random_particles[:,0] = 0
random_particles[:,1] = x
random_particles[:,2] = y


particles = np.zeros((len(x),3))
particles[:,0] = 1/len(x)
particles[:,1] = x
particles[:,2] = y

# Checks to see if a particle is in bounds of a sensor
def check(sensor_coordinates, particles_coordinates):
    return ((particles_coordinates[0]-sensor_coordinates[0])**2 + (particles_coordinates[1]-sensor_coordinates[2])**2 <= .25)

######## LABELS FOR SENSORS ########
dict_sensorcoords = {0: [1.5,0,-2.67000008],
                     1: [0.270000011,0,-2.5],
                     2: [-1.44000006,0,-2.71000004],
                     3: [1.5,0,-1.5], 
                     4: [-1.5,0,-1.5], 
                     5: [1.25999999,0,-0.5], 
                     6: [0,0,-0.5],
                     7: [-1.5,0,-0.5],
                     8: [6,0,-2.31999993],
                     9: [5.5999999,0,-3.5],
                     10: [3.29999995,0,-2.31999993],
                     11: [6,0,-1.31999993],
                     12: [3.29999995,0,-1.31999993],
                     13: [6,0,-0.319999933],
                     14: [4.80000019,0,-0.319999933],
                     15: [3.5999999,0,-0.319999933],
                     16: [4.5999999,0,-3.5],
                     17: [3.5,0,-3.5],
                     18: [3.5,0,-4.69999981],
                     19: [2.5999999,0,-10.3900003], 
                     20: [1.35000002,0,-9.23999977], 
                     21: [1.36000001,0,-10.3100004], 
                     22: [3.63000011,0,-7.97000027], 
                     23: [2.57999992,0,-9.25], 
                     24: [3.63000011,0,-6.97000027], 
                     25: [2.63000011,0,-7.98999977], 
                     26: [3.74000001,0,-9.76000023], 
                     27: [4.03000021,0,4.51999998], 
                     28: [2.59000015,0,4.51999998], 
                     29: [1.38999987,0,4.51999998], 
                     30: [2.59000015,0,2.6099999], 
                     31: [1.38999987,0,2.6099999]}

# Load the numpy file for the sensor readings
sensor_arr = np.load("sensor_array_0.npy")
# Instantiate the array for all the coordiante
arr = []
# Go through each time step
for t in range(sensor_arr.shape[1]):
    # Check which sensors are activated
    sensor_ind_arr = np.where(sensor_arr[:,t] == 1)[0]
    # recalculate the probability for each particles for the select sensors
    for p in range(particles.shape[0]):
        for sens_id in sensor_ind_arr:
            if(check(dict_sensorcoords[sens_id], (particles[p][1], particles[p][2]))):
                particles[p][0] = 1
                break
            else:
                particles[p][0] = 0
        
    # normalize probabilities
    if np.sum(particles[:,0]) == 0:
        resampledInds = np.random.choice(particles.shape[0], size=int(particles.shape[0] * 0.8))
    else:
        normal_prob = particles[:,0]/np.sum(particles[:,0])
        resampledInds = np.random.choice(particles.shape[0], size=int(particles.shape[0] * 0.8), p=normal_prob)

    new_particles = np.zeros(particles.shape,)
    for l in range(int(particles.shape[0] * 0.8)):
        new_particles[l] = particles[resampledInds[l]]
    for l in range(int(particles.shape[0] * 0.2)):
        random_ind = np.random.randint(0, random_particles.shape[0])
        new_particles[int(particles.shape[0] * 0.8)+l] = random_particles[random_ind]

    # Compute weighted average for the particles
    if np.sum(particles[:,0]) == 0:
        avg_x = 0
        avg_y = 0
        avg_c = 0
        for part in particles:
            if True:
                avg_x += part[1] * 1
                avg_y += part[2] * 1
                avg_c += 1
    else:
        avg_x = 0
        avg_y = 0
        avg_c = 0
        for part in particles:
            if True:
                avg_x += part[1] * part[0]
                avg_y += part[2] * part[0]
                avg_c += part[0]

    arr.append((round(avg_x/avg_c,7), round(avg_y/avg_c,7)))

print(arr)