import csv
import matplotlib.pyplot as plt
import numpy as np
import re

from sklearn.decomposition import PCA

with open('results.csv','r') as result_file:
	count = 0
	pick_accuracy = 0
	bans_accuracy = 0
	n_results = 0
	mse = 0

	csvreader = csv.reader(result_file) 
	next(csvreader) # ignoring header
	result_matrix = []
	for line in csvreader:
		# splittig the result line
		n_results += 1
		result = line[0].split(';')

		# extracting the line results
		bans1 = float(result[0])
		bans2 = float(result[1])
		pick1 = float(result[2])
		pick2 = float(result[3])
		victory = True if re.match("True[\n]*",result[4]) is not None else False
		result_matrix.append([(bans1+bans2)/2,(pick1+pick2)/2])

		# calculating the advantages
		team1 = bans1 + pick1
		team2 = bans2 + pick2
		pick_accuracy += pick1 + pick2
		bans_accuracy += bans1 + bans2

		# verifying the result
		if team1 >= team2 and victory:
			count += 1
			mse += team1 - team2
		elif team2 >= team1 and not victory:
			count += 1
			mse += team2 - team1
		elif team1 >= team2 and not victory:
			mse += 2 - team1
		elif team2 >= team1 and victory:
			mse += 2 - team2
	result_matrix = np.array(result_matrix)

	print('Win Conditions')
	print('| Picks and Bans -> Win?',float(count)/float(n_results))
	print('| What is the MSE?',float(mse)/(2*float(n_results)))

	print('Our accuracy')
	print('| Picks accuracy:',float(pick_accuracy)/(2*float(n_results)))
	print('| Bans accuracy:',float(bans_accuracy)/(2*float(n_results)))
	print('| Total accuracy:',float(bans_accuracy + pick_accuracy)/(4*float(n_results)))

	scatter_set = [(r[0],r[1]) for r in result_matrix]
	scatter = list(set(scatter_set))
	counter = [25*scatter_set.count(r) for r in scatter]
	print(counter)
	scatter = np.array([r[0],r[1]] for r in scatter)
	plt.scatter([r[0] for r in result_matrix], [r[1] for r in result_matrix] , marker='o', s=counter)
	plt.xlabel('Ban Hit Rate',size=20)
	plt.ylabel('Pick Hit Rate',size=20)
	plt.show()

	print('Results Insights')
	pca = PCA(n_components=2)
	pca.fit(result_matrix)
	print(pca.explained_variance_ratio_)  
	print(pca.singular_values_)

with open('results.csv','r') as result_file:
	csvreader = csv.reader(result_file) 
	next(csvreader) # ignoring header
	for line in csvreader:
		# splittig the result line
		n_results += 1
		result = line[0].split(';')

		# extracting the line results
		bans1 = float(result[0])
		bans2 = float(result[1])
		victory = True if re.match("True[\n]*",result[4]) is not None else False

		# calculating the advantages
		team1 = bans1
		team2 = bans2
		bans_accuracy += bans1 + bans2

		# verifying the result
		if team1 >= team2 and victory:
			count += 1
			mse += team1 - team2
		elif team2 >= team1 and not victory:
			count += 1
			mse += team2 - team1
		elif team1 >= team2 and not victory:
			mse += 1 - team1
		elif team2 >= team1 and victory:
			mse += 1 - team2

	print('Win Conditions')
	print('| Picks and Bans -> Win?',float(count)/float(n_results))
	print('| What is the MSE?',float(mse)/(2*float(n_results)))

	print('Our accuracy')
	print('| Accuracy:',float(bans_accuracy)/(2*float(n_results)))