import sys
import random
from operator import itemgetter
from random import randint
train_data =  sys.argv[1]
label_data = sys.argv[2]
test_data =  sys.argv[3]
test_label = sys.argv[4]

def learning_rate(t,r,c):
	rate_t= r/float(1+(r*t/c))
	return rate_t

def svm_prediction(final_data,feature_length,bias,weight,rate_r,C):
	false_count =0
	true_count =0
	dot_product=[]
	t_count =0
	for i in final_data:
		t_count+=1
		rate=learning_rate(t_count,rate_r,C)
		i = [float(j) for j in i ]
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product
		if(derived_label*i[-1] <= 1):
			product=map(lambda x: x*i[-1]*rate*C,i[:-1])
			weight_r = map(lambda x: x*(1-rate), weight)
			weight=map(lambda x,y:x+y ,weight_r,product)
			false_count+=1
		else:			
			weight = map(lambda x: x*(1-rate), weight)
			true_count+=1
	return weight, false_count

def read_file(train_data,label_data):
	data = []
	label = []
	final_data = []
	with open(train_data) as data_file:
		for line in data_file:
				line=line.split()
				data.append(line)
	with open(label_data) as label_file:
		for line in label_file:
				line = line.split()
				label.append(line)
	length_data = len(data)
	for i in range(length_data):
		data[i].insert(0,1)	
	feature_length = len(max(data,key=len))
	for i in range(length_data):
		data[i].append(label[i][-1])
	return data,length_data,feature_length

def calculate_accuracy_cross_validation(data_test_file,weight):
	false_count =0
	true_count =0
	dot_product=[]
	for i in data_test_file:
		i = [float(j) for j in i ]
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product
		if(derived_label*i[-1] > 0):
			true_count+=1
			#j= j+1
		else:
			#j+=1
			false_count+=1
	#print "No of mistakes on Test data: ",false_count
	accuracy_data=(true_count/float(true_count+false_count))
	return accuracy_data

def calculate_accuracy(weight):
	false_count =0
	true_count =0
	dot_product=[]
	#bias=0
	#j=0
	data_test_file=[]
	data_test_file,length_data,feature_length=read_file(test_data,test_label)
	for i in data_test_file:
		i = [float(j) for j in i ]
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product 
		if(derived_label*i[-1] > 0):
			true_count+=1
			#j= j+1
		else:
			#j+=1
			false_count+=1
	print "True Count :",true_count,"False count : ",false_count
	accuracy_data=(true_count/float(true_count+false_count))
	return accuracy_data

def cross_validation(final_data,data_len,count):
	no_of_splits =data_len/5
	Set_a =final_data[:no_of_splits]
	Set_b =final_data[no_of_splits:2*no_of_splits]
	Set_c =final_data[2*no_of_splits:3*no_of_splits]
	Set_d = final_data[3*no_of_splits:4*no_of_splits]
	Set_e =final_data[4*no_of_splits:5*no_of_splits]
	if (count == 0):
		final_data = Set_b + Set_c + Set_d + Set_e
		return Set_a , final_data
	elif (count == 1):
		final_data = Set_a + Set_c + Set_d + Set_e
		return Set_b , final_data
	elif (count == 2):
		final_data = Set_a + Set_b + Set_d + Set_e
		return Set_c , final_data
	elif (count == 3):
		final_data = Set_a + Set_b + Set_c + Set_e
		return Set_d , final_data
	elif (count == 4):
		final_data = Set_a + Set_b + Set_c + Set_d
		return Set_e , final_data

def main():
	bias = 0
	final_data_initial, data_len, feature_length = read_file(train_data,label_data)
	weight_vector = [0]*(feature_length-1)
	weight_vector.insert(0,bias)
	weight_vector = [ float(x) for x in weight_vector]
	C_list=[0.70, 0.75, 0.80, 0.85, 0.90,0.95]
	rate_r_list=[0.50, 0.60, 0.70]
	super_list =[]
	#super_super_list =[]
	epoch=[3,5,8]
	for i in epoch:
		for j in range(i):
			updates_final=0
			random.shuffle(final_data_initial)
			#for count in range(5)
			#count = random.randint(1,5)
			#print "count : ",count,"\n"
			#test_data,final_data=cross_validation(final_data_initial,data_len,count)
			for l_rate in rate_r_list:
				for c_value in C_list:
					for count in range(5):
						test_data,final_data=cross_validation(final_data_initial,data_len,count)
						weight_vector, updates =svm_prediction(final_data,feature_length,bias,weight_vector,l_rate,c_value)
						updates_final = updates_final + updates
						accuracy =calculate_accuracy_cross_validation(test_data,weight_vector)
						super_list.append([l_rate,c_value,format(accuracy*100,'.3f')])
					#super_list = sorted(super_list, key=itemgetter(2),reverse = True)
					#print "rate: ",l_rate,"C: ",c_value, "Accuracy: ",accuracy,"\n"
	print "------------------------------------------------------------------------"					
	print super_list
	print "------------------------------------------------------------------------"
	super_list = sorted(super_list, key=itemgetter(2),reverse = True)
	print "final parameters after cross validation : ",super_list[0]
	print "rate: ",super_list[0][0],"C: ",super_list[0][1], "Accuracy: ",super_list[0][2]
	#print "Test Data ----------------------\n"
	epoch=[3,5,8]
	for i in epoch:
		for j in range(i):
			updates_final=0
			random.shuffle(final_data_initial)
			#rate=learning_rate(j,r,C)
			weight_vector, updates =svm_prediction(final_data_initial,feature_length,bias,weight_vector,super_list[0][0],super_list[0][1])
			updates_final = updates_final + updates
		#print "Weight Vector:",weight_vector
		print "-------------------------------------------------"
		print "Total no of updates :", updates_final
		#print "----------------------",weight_vector,"------------------------------" 
		accuracy =calculate_accuracy(weight_vector)
		print "-------------------------------------------------"
		print "Accuracy on Test Data is:",accuracy*100," for epoch",i
	
main()