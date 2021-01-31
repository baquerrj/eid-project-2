
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots() 

ax.plot([1,2,3,4], [1,4,2,3])

ax.plot([1,2,3,4], [4,3,2,1])
plt.xlabel('measurements')
plt.ylabel('temperature')

plt.show()