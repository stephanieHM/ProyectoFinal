
import matplotlib.pyplot as plt # For visualizing the data and error
from sklearn import datasets #Sklearn library for load data
import numpy as np #Numpy array
from matplotlib.colors import ListedColormap # Content list of color for plotting
from scipy.io import wavfile

### LOAD NOISE DATASET

fs, noise = wavfile.read('whitenoise.wav')
L = len(noise)
c = np.fft.fft(noise) # create a list of complex number
print "c is"
print c

freqnueva=(np.abs(c[:len(c)]))
print "frecuencia nueva"

print freqnueva
plt.plot(freqnueva[:500])
plt.show()


freq = np.fft.fftfreq(L)

np.savetxt('archivo.txt', freq, fmt='%.4e')

freq2 = (np.abs(c[:len(c)]))
plt.plot(freq2[:500])
plt.title('freq 2')
plt.show()




#freq = np.linspace(0, 1/(2L), L/2)
print ("frecuencia 1 con transformada ")
print freq

	
freq_in_hertz = abs(freq * fs)
print ("frecuencia en hertz ")
print freq_in_hertz
print ("abs(c) ")
print abs(c)
print len(freq_in_hertz)


plt.plot(freq_in_hertz[:500], abs(c)[:500])
plt.title('freq in hertz vs abs')
plt.show()


### Load iris dataset
# iris_datasets = datasets.load_iris()
# print iris_datasets

### Using 100 first samples with 2 features
X = freq_in_hertz
# X = iris_datasets.data[:100, 2:] # We only the two features: petal length and petal width
y = abs(c)
# y = iris_datasets.target[:100] # The target flowers with setosa = 0 and versicolor = 1

### Assume labels of Setosa(0) is -1 and Versicolor = 1
### it's just represent the theory we've learned for better intuition
### and void dealing with 0 that maybe cause incorrect when we classify
# for i in range(50):
  #   y[i] = -1

### Scatter plot iris data
### The red dots ----> Setosa (-1)
### The blue dots ----> Versicolor (1)
# cm_bright = ListedColormap(['#FF0000', '#0000FF'])
# plt.figure(figsize=(7,5))
# plt.scatter(X[:,0], X[:,1], c=y, cmap=cm_bright)
# plt.scatter(None, None, color = 'r', label='Setosa')
# plt.scatter(None, None, color = 'b', label='Versicolor')
# plt.legend()
# plt.title('Visualize the data')
# plt.xlabel('Petal length')
# plt.ylabel('Petal width')
# plt.show()

class Adaline(object):
    def __init__(self, eta = 0.001, epoch = 100):
        self.eta = eta
        self.epoch = epoch

    def fit(self, X, y):
        np.random.seed(16)
        self.weight_ = np.random.uniform(-1, 1, X.shape[0] + 1)# X.shape[1] 
        self.error_ = []
        
        cost = 0
        for _ in range(self.epoch):
            
            output = self.activation_function(X)
            error = y - output
            
            self.weight_[0] += self.eta * sum(error)
            self.weight_[1:] += self.eta * X.T.dot(error)
            
            cost = 1./2 * sum((error**2))
            self.error_.append(cost)
            
        return self

    def net_input(self, X):
        """Calculate the net input z"""
        return np.dot(X, self.weight_[1:]) + self.weight_[0]
    def activation_function(self, X):
        """Calculate the output g(z)"""
        return self.net_input(X)
    def predict(self, X):
        """Return the binary value 0 or 1"""
        return np.where(self.activation_function(X) >= 0.0, 1, -1)


###Plot the error after 100 epochs
names = ['Choose the learning rate eta = 0.001', 'Choose the learning rate eta = 0.01']
classifiers = [Adaline(), Adaline(eta = 0.01)]
step = 1
plt.figure(figsize=(14,5))
for name, classifier in zip(names, classifiers):
    ax = plt.subplot(1, 2, step)
    clf = classifier.fit(X, y)
    print ("clf.error es")
    print clf.error_
    ax.plot(range(len(clf.error_)), clf.error_)
    ax.set_ylabel('Error')
    ax.set_xlabel('Epoch')
    ax.set_title(name)

    step += 1

plt.show()
