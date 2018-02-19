import math

def read_data():
	attributes=[]
	labels=[]
	data=[]
	with open("/home/sarvagya/Documents/Machine Learning/datasets/SettingB/training.data") as doc:
		for line in doc:
			line=line.replace(",","")
			line=line.split()
			data.extend(line)
			attributes.append(line[0][:-1])
			labels.append(line[0][-1])

	return attributes,labels,data

def read_test_data():
	test_attributes=[]
	test_labels=[]
	test_data=[]
	with open("/home/sarvagya/Documents/Machine Learning/datasets/SettingA/test.data") as doc:
		for line in doc:
			line=line.replace(",","")
			line=line.split()
			test_data.extend(line)
			test_attributes.append(line[0][:-1])
			test_labels.append(line[0][-1])

	return test_attributes,test_labels,test_data


def calculate_unique(labels):
	unique={}
	data_entropy=0.0
	for elem in labels:
		if elem in unique:
			unique[elem]=unique[elem]+1
		else:
			unique[elem]=1

	return unique

def calculate_gain(labels,tuples):
	labels=tuples["total"]
	del tuples["total"]
	entropy=calculate_entropy(labels,tuples)

	return entropy
	
def gain(data,single_attribute,column,total_entropy,dict_for_entropy):
	unique=calculate_unique(single_attribute)

	occurences={}
	for elem in data:
		if elem[column] in unique:
			if elem[column] in occurences:				
				if elem[-1] in occurences[elem[column]]:
					occurences[elem[column]][elem[-1]]=occurences[elem[column]][elem[-1]]+1
					occurences[elem[column]]["total"]=occurences[elem[column]]["total"]+1
				else:
					occurences[elem[column]][elem[-1]]=1
					occurences[elem[column]]["total"]=occurences[elem[column]]["total"]+1
			else:
				occurences[elem[column]]={elem[-1]:1}
				occurences[elem[column]]["total"]=1

	info_gain=0.0
	for keys in occurences:
		Dj=occurences[keys]["total"]
		D=len(data)
		info_gain=info_gain+(float(Dj)/D)*calculate_gain(len(single_attribute),occurences[keys])
	dict_for_entropy[total_entropy-info_gain]=column
	return total_entropy-info_gain,dict_for_entropy

def choose_best_attribute(data,list_of_attributes,class_labels,gain):
	unique=calculate_unique(class_labels)
	total_entropy=calculate_entropy(len(class_labels),unique)
	best_gain=0.0
	entropy_results={}
	
	for i in range(len(list_of_attributes[0])):
		label_by_label=[]
		for j in range(len(list_of_attributes)):
			label_by_label.append(list_of_attributes[j][i])
		
		info_gain,entropy_results=gain(data,label_by_label,i,total_entropy,entropy_results)
		if info_gain>best_gain:
			best_gain=info_gain
		else:
			continue

	return(entropy_results[best_gain])


def calculate_entropy(labels,unique):
	data_entropy=0.0
	for frequency in unique.values():
		data_entropy -= (float(frequency)/labels) * math.log(float(frequency)/labels, 2)


	return data_entropy 

def get_best_attribute(data,best_column):
	best_attribute=[]
	for i in range(len(data)):
		best_attribute.append(data[i][best_column])
	
	return best_attribute	

def get_examples(data,best_attribute,best_column_number,class_labels):
	unique=calculate_unique(best_attribute)
	respective_values=[]
	for val in unique:
		for elem in range(len(data)):
			if val==data[elem][best_column_number]:
				respective_values.append([val,data[elem][-1],elem])

	values_dict={}
	for elem in respective_values:
		if (elem[0]) in values_dict:
			values_dict[elem[0]].append(elem[2])
		else:
			values_dict[elem[0]]=[elem[2]]

	respective_values_list=[]
	for a in values_dict:
		respective_values_list.append([a,values_dict[a]])

	return respective_values_list

def get_values(elem,data,best):
	temp_data=[]
	derived_data=[]
	for i in elem[1]:
		temp_data.append(data[i])

	for i in temp_data:
		derived_data.append(i[:best]+i[best+1:])

	return derived_data			
	
def create_tree(data,list_of_attributes,class_labels,gain):
	unique=calculate_unique(i[-1] for i in data)
	max=0
	most_frequent=None
	for keys in unique:
		if unique[keys]>max:
			max=unique[keys]
			most_frequent=keys

	if not data or (len(list_of_attributes) - 1) <= 0:
		return	most_frequent

	elif class_labels.count(class_labels[0])==len(class_labels):
		return class_labels[0]

	else:
		best=choose_best_attribute(data,list_of_attributes,class_labels,gain)
		best_attribute=get_best_attribute(data,best)
		tree={best:{}}
		respective_values_list=get_examples(data,best_attribute,best,class_labels)
		
		for elem in respective_values_list:

			derived_list_of_attributes=[]
			derived_data=get_values(elem,data,best)
			derived_class_labels=[i[-1] for i in derived_data]
			for i in derived_data:
				derived_list_of_attributes.append(i[:-1])

		
			tree[best][elem[0]]=create_tree(derived_data,derived_list_of_attributes,derived_class_labels,gain)
	return tree

def get_classification(record,tree,i):
	if type(tree) == type("string"):
		return tree
	
	else:
		attr = tree.keys()[0]
		if record[attr] in tree[attr]:
			t = tree[attr][record[attr]]
			new_record=record[:attr]+record[attr+1:]
		else:
			return "x"

		return get_classification(new_record, t,i)

def classify(tree,test_data):
	classification=[]
	for record in test_data:
		classification.append(get_classification(record, tree,0))
	return classification


def main():
	data=[]
	list_of_attributes,class_labels, data=read_data()
	tree=create_tree(data,list_of_attributes,class_labels,gain)
	#print tree
	test_attributes,test_class_labels,test_data=read_test_data()
	classification=classify(tree,test_data)
	positive=0
	negative=0
	for i in range(len(classification)):
		if classification[i]==test_data[i][-1]:
			positive+=1
		else:
			negative+=1

	total=positive+negative
	print float(positive)/total


		

	

main()



#--------------------------------------MAKE TREE AND SAY YAYY!