
import matplotlib.pyplot as plt
import numpy as np

# Simple data to display in various forms
x = np.linspace(0, 2 * np.pi, 1024)
y = np.sin(x*2)#+np.sin(x*100)*0.02	
yf=np.fft.fft(y)
plt.close('all')



# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(x, y)
axarr[0].set_title('Sharing X axis')
axarr[1].scatter(x, yf)

plt.show()
