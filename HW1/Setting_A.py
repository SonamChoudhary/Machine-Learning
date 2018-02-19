import math
import sys
setting_A = sys.argv[1]
setting_B = sys.argv[2]

#*****************entropy of the dataset_setting A***************************
#***************************************entropy formula**********************
def entropy_cal(x,y):
		prob_x = (float(x)/(x+y))
		prob_y = (float(y)/(x+y))
		log_x = math.log(prob_x,2)
		log_y = math.log(prob_y,2)
		entropy = -float(prob_x*log_x)-float(prob_y*log_y)
		return entropy
#*********************************************rntropy of the data*******************************
def entropy_data(labels):
	count_l = labels
	counter = {u:count_l.count(u) for u in count_l}
	count_label = []
	count_label = counter.values()
	if (len(count_label) <= 1):
		entropy_total = 0
	else:
		entropy_total = entropy_cal(count_label[0],count_label[1])	
	return entropy_total

#**************************************Selecting best attribute*************************************************
def best_attri(data):
	labels=[]
	for i in data:
		labels.append(i[-1])
	e_label=entropy_data(labels)
	best_gain_col=entropy_rest_attributes(data,e_label)
	return best_gain_col  	


#**************************************Entropy of attributes apart from label***********************************
def entropy_rest_attributes(data,e_label):
	list_A=data
	list_count = []
	temp_list=[]
	frequency_list=[]
	#i=0
	e_total = e_label
	best_gain=[]
	final_results=[]
	column=0
	for i in range(len(list_A[0])-1):
		temp_list=[]
		list_count=[]

		for j in range(len(list_A)):
			concat_element=list_A[j][i]+list_A[j][-1]
			temp_list.append(concat_element)
			list_count.append(temp_list.count(concat_element))
		
		best_gain=attribute_entropy(temp_list,list_count,column,e_total,best_gain)
		final_results.extend(best_gain)
		#print best_gain
		column=column+1
	#print final_results
	return max(final_results)[1]
	#return best_gain_col

#**************************************Info-gain for the attributes**********************************************

def attribute_entropy(list_A1,list_count,column,e_total,best_gain):
	list_Attri = []
	list_value = []
	dict_atri_entropy = dict()
	dict_y = dict(zip(list_A1,list_count))
	list_keys = dict_y.keys()
	atri_no = 1
	default_y = 0
	list_info_gain = []
	info_gain = 0

	for k in list_keys:
		j=1	
		for j in list_keys:
			if k[0] == j[0] and k != j :
				if str([j,k]) not in list_Attri:
					list_Attri.append(str([k,j]))
					total = dict_y[k]+dict_y[j]
					entropy_A1 = entropy_cal(dict_y[k],dict_y[j])
					list_value.append(str([dict_y[k],dict_y[j],total,entropy_A1]))
					total_data_count = len(list_A1)
					info_gain += (total/float(total_data_count))*float(entropy_A1)
	best_gain = []
	information_gain = e_total-info_gain
	best_gain.append([information_gain,column])
	return best_gain

#**************************************************Get uniques values of the best_column************************
def find_unique(column_best,data):
	unique = {}
	for i in range(len(data)):
		if data[i][column_best] in unique:
			unique[data[i][column_best]]+=1
		else:
			unique[data[i][column_best]]=1
	return unique

#****************************************************Derive data*************************************************
def derive_data(key,column_best,data):
	derived_list={}
	final_list=[]
	for i in range(len(data)):
		if data[i][column_best] == key:
			if key in derived_list:
				derived_list[key].append(data[i])
			else:
				derived_list[key]=[data[i]]

	return derived_list

#*****************************************************recursion condition****************************************
def cal_unique_recursion(labels):
	unique={}
	data_entropy=0.0
	for elem in labels:
		if elem in unique:
			unique[elem]=unique[elem]+1
		else:
			unique[elem]=1

	return unique

#*******************************************create tree**********************************************************

def get_data(derived_list,column_best):
#	for elem in derived_list:
	new_data=[]
	maha_new_data=[]
	values=[]
	for keys in derived_list:
		values=derived_list[keys]		
	for elem in values:
		new_data.append(elem)
	for elem in new_data:
		temp=elem[:column_best]+elem[column_best+1:]
		maha_new_data.append(elem[:column_best]+elem[column_best+1:])
	return maha_new_data

#***********************************************************create tree**************************************************************
def tree_creation(data,attribute_list):
	label=[]
	for i in data:
		label.append(i[-1])
	uniq = cal_unique_recursion(label)
	max = 0
	most_frequent=None

	for i in uniq.keys():
		if uniq[i]>max:
			max=uniq[i]
			most_frequent=i
	
	if not data or (len(attribute_list) - 1) <= 0:
		return	most_frequent

	elif label.count(label[0])==len(label):
		return label[0]	

	else:
		data_derived = []
		labels =[]
		for i in data: 
			labels.append(i[-1])
		entropy_label =entropy_data(labels)
		column_best = best_attri(data)
		tree={column_best:{}}

		unique=find_unique(column_best,data)
		new_attribute_list=[]
		for key in unique.keys():
			derived_list = derive_data(key,column_best,data) 
			derived_data=get_data(derived_list,column_best)
			for i in range(len(derived_data)):
				new_attribute_list.append(derived_data[i][:-1])
			
			tree[column_best][key]=tree_creation(derived_data,new_attribute_list)
	return tree

#*******************************************Testing****************************************************************
def training_tree():
	list_A = []
	list_B = []
	attribute =[]
	with open(setting_B,'r') as data_file:
		for line in data_file:
			line=line.replace(",","")
			line=line.split()
			list_A.extend(line)
	return list_A    

#******************************************Training data file read*************************************************

def main_data():
	global list_A
	list_A = []
	list_B = []
	attribute =[]
	with open(setting_A,'r') as data_file:
		for line in data_file:
			line=line.replace(",","")
			line=line.split()
			list_A.extend(line)
			attribute.append(line[0][:-1])
		#print list_A
		return list_A,attribute

#*****************************************Tree-Training************************************************************
def get_test_results(row,tree):
	
	if type(tree) == type("string"):
		return tree
	else:
		a = tree.keys()[0]
		if row[a] in tree[a]:
			tree_nw = tree[a][row[a]]
			record_nw=row[:a]+row[a+1:]
		else:
			return "Not found"

		return get_test_results(record_nw,tree_nw)

#***********************************************************************************************************************
def get_final_list(tree,test_data):
	final_list=[]
	for row in test_data:
		final_list.append(get_test_results(row,tree))
	return final_list

    		
#*******************************************************Main Function********************************************************    		
def main():
    data,attribute_list = main_data()
    tree = tree_creation(data,attribute_list)
    print tree
    training_test_data = training_tree()
    list_f=get_final_list(tree,training_test_data)
    Total_count_match=0
    Total_count_no_match=0
    for i in range(len(list_f)):
    	if list_f[i]==training_test_data[i][-1]:
    		Total_count_match+=1
    	else:
    		Total_count_no_match+=1
    total=Total_count_match+Total_count_no_match
    test_result = float(Total_count_match)/total
    print "TEST_RESULT : ", test_result

    

    
main()