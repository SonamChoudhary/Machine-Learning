import math
import random
from random import randint
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
	new_data=[]
	labels=[]
	for i in data:
		labels.append(i[-1])
	e_label=entropy_data(labels)
	column =[]
	"""for num in range(9):
		count=random.randint(1,255)
		column.append(count)
	#for col in column:
	print type(data[0][0]),"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	#print column,"----------columns selected-----------------",len(data)
	for i in range(len(data)):
		for j in range(len(data[0])):
			#print data[i] ,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			if j not in column: 
			#	print j
			#	print type(data[i]),"----------type---------------",data[i]
			#	print data[i][j],"~~~~~~~~~~~~~~~~~~~~~~~~"
				data[i]=data[i].remove(data[i][j])
			#	print data[i],"---------------------------------------------"""
		
	best_gain_col=entropy_rest_attributes(data,e_label)
	return best_gain_col  	


#**************************************Entropy of attributes apart from label***********************************
def entropy_rest_attributes(list_A,e_label):
	#list_A=data
	#print len(list_A[0]),(len(list_A)),"-------------------------------------------"
	list_count = []
	temp_list=[]
	frequency_list=[]
	#i=0
	e_total = e_label
	best_gain=[]
	final_results=[]
	column = []
	#col_size = 255
	for j in range(9):
		count=random.randint(0,len(list_A[0])-1)
		column.append(count)
	#for i in range(len(list_A[0])-1):
	#col_size-=1
	#print "Column list:---------------",column
	for i in column:
		temp_list=[]
		list_count=[]
		for j in range(len(list_A)):
			#print "j:",j,"  i:",i ,"length of List_A: ", len(list_A[0]) ,"****************************"
			#print list_A[j][i] ,list_A[j][-1],"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			concat_element=list_A[j][i]+list_A[j][-1]
			temp_list.append(concat_element)
			list_count.append(temp_list.count(concat_element))
		#print temp_list,"----------------------------"
		#for col in column: 
		#for i in range(len(list_A)):
			#for j in range(len(list_A[i])):
				#if j not in column:
				#	temp_list[i]=temp_list[i].remove(temp_list[i][j])
		best_gain=attribute_entropy(temp_list,list_count,i,e_total,best_gain)
		final_results.extend(best_gain)
		#print best_gain
		#column=column+1
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
		#print len(data),"---------------------------------length",len(data[i])
		#print i,"------",column_best
		#print i,column_best , data[i][column_best]
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
		entropy_label = entropy_data(labels)
		column_best = best_attri(data)
		tree={column_best:{}}
		#print "tree creation---------------------data length-----------------",len(data),column_best
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
def test_train_tree():
	list_A = []
	list_B = []
	attribute =[]
	label =[]
	"""with open("train.data",'r') as data_file:
		for line in data_file:
			#line=line.replace(",","")
			line=line.split()
			list_A.append(line)
	with open("train.labels",'r') as label_file:
		for line in label_file:
				line = line.split()
				label.append(line)
	length_data = len(attribute)
	for i in range(length_data):
		list_A[i].append(label[i][-1])"""

	with open("train.data",'r') as data_file:
		for line in data_file:
			#line=line.replace(",","")
			line=line.split()
			list_A.append(line)
			attribute.append(line)
		#print list_A
	with open("train.labels",'r') as label_file:
		for line in label_file:
			line = line.split()
			label.append(line)
	length_data = len(attribute)
	#for i in range(length_data):
		#data[i].insert(0,1)	
	#feature_length = len(max(data,key=len))
	for i in range(length_data):
		list_A[i].append(label[i][-1])
	#print list_A[:4]

	return list_A    
#**********************************************************Test File****************************************
def test_test_tree():
	list_A = []
	list_B = []
	attribute =[]
	label =[]
	with open("test.data",'r') as data_file:
		for line in data_file:
			#line=line.replace(",","")
			line=line.split()
			list_A.append(line)
			attribute.append(line)
		#print list_A
	with open("test.labels",'r') as label_file:
		for line in label_file:
			line = line.split()
			label.append(line)
	length_data = len(attribute)
	#for i in range(length_data):
		#data[i].insert(0,1)	
	#feature_length = len(max(data,key=len))
	for i in range(length_data):
		list_A[i].append(label[i][-1])
	#print list_A[:4]

	return list_A   


#******************************************Training data file read*************************************************

def main_data():
	global list_A
	list_A = []
	list_B = []
	attribute =[]
	label =[]
	final_svm_data_list=[]
	with open("train.data",'r') as data_file:
		for line in data_file:
			#line=line.replace(",","")
			line=line.split()
			list_A.append(line)
			attribute.append(line)
		#print list_A
	with open("train.labels",'r') as label_file:
		for line in label_file:
				line = line.split()
				label.append(line)
	length_data = len(attribute)
	#for i in range(length_data):
		#data[i].insert(0,1)	
	#feature_length = len(max(data,key=len))
	for i in range(length_data):
		list_A[i].append(label[i][-1])
	#return data,length_data,feature_length
	#print "----------------------------main data---------------------",list_A[:5]
	return list_A,attribute,length_data

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
	list_data_svm_test=[]
	final_svm_data_list=[]
	list_data_svm=[]
	data=[]
	attribute_list =[]
	complete_data,attribute_list_complete,length_data=main_data()
	#print complete_data[:4],"----------------------"
	for k in complete_data:
		for l in k:
			l=float(l)
	#print k
	#print type(complete_data[0][0]),"------------type---------------------"	
	for i in range(5):
		for j in range(600):
			count = random.randint(0,length_data-1)
			#print count ,"------->",complete_data[count],"---------------"
			data.append(complete_data[count])
			attribute_list.append(complete_data[count][:-1])
		#print data[0][254],"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`"
		tree = tree_creation(data,attribute_list)
		#print "---------------------------------------------"
		#print tree
		test_train_data = test_train_tree()
		#test_train_data = test_test_tree()
		list_f_train=get_final_list(tree,test_train_data)
		#print list_f ,"----------------------------------------------" ,training_test_data
		#print training_test_dat
		Total_count_match=0
		Total_count_no_match=0
		for i in range(len(list_f_train)):
			if list_f_train[i]==test_train_data[i][-1]:
				#print test_train_data[i][-1] ,"---------------label"
				Total_count_match+=1
			else:
				Total_count_no_match+=1
		total=Total_count_match+Total_count_no_match
		test_result = float(Total_count_match)/total
		print "Accuracy training data : ", test_result
		list_data_svm.append(list_f_train)
		#print len(list_data_svm),"----------------------------------------"
		#for i in list_data_svm:
		final_train=[]
		for j in range (len(list_data_svm[0])):
			final_svm_data_list=[]
			for k in list_data_svm:
				final_svm_data_list.append(k[j])
			final_train.append(final_svm_data_list)
			#print len(final),"---------------------"
			#return final    
		test_test_data=test_test_tree()
		list_f_test=get_final_list(tree,test_test_data)
		#print list_f ,"----------------------------------------------" ,training_test_data
		#print training_test_dat
		Total_count_match_test=0
		Total_count_no_match_test=0
		for i in range(len(list_f_test)):
			if list_f_test[i]==test_test_data[i][-1]:
				#print test_test_data[i][-1] ,"---------------label"
				Total_count_match_test+=1
			else:
				Total_count_no_match_test+=1
		total=Total_count_match_test+Total_count_no_match_test
		test_result_test = float(Total_count_match_test)/total
		print "Accuracy : ", test_result_test
		list_data_svm_test.append(list_f_test)
		#print len(list_data_svm),"----------------------------------------"
		#for i in list_data_svm:
		final_test=[]
		for j in range (len(list_data_svm_test[0])):
			final_svm_data_list_test=[]
			for k in list_data_svm:
				final_svm_data_list_test.append(k[j])
			final_test.append(final_svm_data_list_test)

	return final_train,final_test

    
#main()