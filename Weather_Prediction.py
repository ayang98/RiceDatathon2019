import pandas as pd
import numpy as np
from collections import Counter
from collections import defaultdict
import heapq as hq
import matplotlib.pyplot as plt

df1 = pd.read_csv("pressure.csv")
data1 = df1[['Houston']]
data1 = np.array(data1)

df2 = pd.read_csv("humidity.csv")
data2 = df2[['Houston']]
data2 = np.array(data2)

df3 = pd.read_csv("temperature.csv")
data3 = df3[['Houston']]
data3 = np.array(data3)

df4 = pd.read_csv("wind_speed.csv")
data4 = df4[['Houston']]
data4 = np.array(data4)


data = np.hstack(np.array([data1, data2, data3, data4]))

data = data[1:, :]

#print final


df5 = pd.read_csv("weather_description.csv")
data5 = df5[['Houston']]
data5 = np.array(data5)

output = data5[1:,:]


list1 = []

for element in output:
	list1.append(str(element))


unique = list(set(list1))


dict1 = {}
for i in range(len(unique)):
	dict1[unique[i]] = i

rows = output.shape[0]

for i in range(rows):

	output[i,:] = dict1[str(output[i,:])]


indices = np.array([range(data.shape[0])])
training = np.hstack((np.transpose(indices), data))

# print training
# print output

def knn(training, test, k, output):
	"""
	training = training data in the form of a numpy matrix where each row represents an entry of data
	test = numpy matrix of data to be tested for outcome knn
	k = k nearest neighbors
	output = corresponding numpy outcome array to each row of training data
	"""
	predicted = [] #the matrix holding the predicted outcomes using knn
	for array1 in test:
		outcomes = defaultdict(int)
		distances = {}
		max_value = 0
		for array2 in training:
			distances[np.linalg.norm(array2[1:]-array1)] = array2
		distances = sorted(distances.items())
		for index in range(k):
			array = distances[index][1]
			# print array, array[0], output[array[0]]
			outcomes[output[int(array[0])][0]] += 1
		for key, value in outcomes.items():
			if value > max_value:
				max_value = value
				max_key = key
		predicted.append(max_key)
	return np.transpose(np.array([predicted]))

# print training[:-data.shape[0]/100]
# print data[-data.shape[0]/100,:]



#Creating testing/graph
#Training data is 95% of the values in dataset; testing data is last 5%
k_values = range(3,154,10)
accuracy = []
a = output[-data.shape[0]/200:] #actually results of the last 5% to be compared for accuracy of prediction
for k in k_values:
	b = knn(training[:-data.shape[0]/200], data[-data.shape[0]/200:], k, output)
	count = 0
	for index in range(len(a)):
		if a[index] == b[index]:
			count += 1

	accuracy.append(count/float(len(b)))
	print count/float(len(b))

plt.scatter(k_values, accuracy)
#plot_lines([model_acc_on_k], 'Varying Sizes of k on Model Prediction Accuracy', 'k (nearest neighbors)', 'Model Prediction Accuracy (Out of 1)', None, 'knn_weather_predict')