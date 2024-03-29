import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import csv


'''
Code to plot Poiseuille flow's simulation velocity profile, 
compared with analytical solution.
'''


def define_poiseuille(k, H, nu):
    def poiseuille(z):
        return k*(H*z - z**2)/(2*nu)
    return poiseuille


def find_max_nb(files, path=''):
    max_nb = 0
    for file in files:
        with open(path + file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                nbs = len(row)
                if nbs > max_nb:
                    max_nb = nbs
    return max_nb


# Parameters
c = 30
alpha = 1
support = 3
h = 0.009231
nu = alpha*c*h/(8*2.7)
print("Nu:", nu)
H = 0.4
k = 0.05

poise = define_poiseuille(k, H, nu)
print("Max real vel:", poise(H*0.5))
z = np.linspace(0, H, 100)
v = poise(z)

# Sort and load files
files = sorted(os.listdir("../log/poise"), key=lambda x: float(re.findall('\d+', x)[0]))
nb = find_max_nb(["../log/poise/{}".format(files[0])])

# Show plot for last simulation step
df = pd.read_csv("../log/poise/{}".format(files[-1]), names=[i for i in range(nb)]).fillna(0)
xvel = df[0].values
zpos = df[1].values
print("Max sim vel:", max(xvel))

fig = plt.figure()
plt.plot(v, z, label='Analítico')
plt.plot(xvel, zpos, 'k.', label='Simulación')
plt.xlabel("Velocidad en eje x")
plt.ylabel("Posición en eje y")
plt.grid()
plt.legend()
plt.show()
plt.close(fig)

# Generate plots for all simulation
# for i, file in enumerate(files):
#     if not i%50:
#         print(i)
#         df = pd.read_csv("log/poise/{}".format(file), names=[i for i in range(nb)]).fillna(0)
#         xpos = df[0].values
#         zvel = df[1].values
#
#         fig = plt.figure()
#         plt.title(file)
#         plt.plot(v, z)
#         plt.plot(xpos, zvel, 'k.')
#         plt.savefig("log/poise_plots/{}".format(i), bbox_inches='tight')
#         plt.close(fig)


