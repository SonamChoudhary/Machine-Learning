import matplotlib.pyplot as plt
import sys
import random
import math
from operator import itemgetter
from random import randint
train_data =  sys.argv[1]
test_data = sys.argv[2]
#test_label = sys.argv[4]

def cal_learning_rate(t,r,sigma_sqr):
	#print type(r),type(t),type(sigma_sqr),"*************************"
	rate_t= r/float(1+(r*t/sigma_sqr))
	return rate_t

#final_data,feature_length,bias,weight,rate_r,C
def prediction(input_data,feature_length,bias,weight,rate,sigma_s):
	#bias = bias_new
	false_count =0
	true_count =0
	dot_product=[]
	j=0
	t_count =0
	neg_likely=0
	for i in input_data:
		
		t_count+=1
		#print type(i),len(i),len(weight),type(weight),"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		final_product = reduce(lambda x,y:x+y ,dot_product)
		#derived_label = final_product + bias
		r_rate=cal_learning_rate(t_count,rate,sigma_s)
		#print i ,"------------------------------input----------------------"

		yx_val = map(lambda x:x*i[-1],i[:-1])
		coef = -1/float(1+(math.exp(i[-1]*final_product)))
		first_term = map(lambda x:x*coef,yx_val)
		w_sigma_sqr = map(lambda x: x*(2/sigma_s),weight)
		update_w=map(lambda x,y:x+y,first_term,w_sigma_sqr)
		final_update = map(lambda x:x*r_rate,update_w)
		weight = map(lambda x,y:x-y,weight,final_update)
		neg_likely=neg_likely+math.log(1+math.exp(-i[-1]*final_product))
		#j+=1
	return weight

def read_file(data_train):
	weight_final=[]
	label = []
	feature_data=[]
	complete_feature_data =[]
	full_size_data=[]
	n=0
	list_data=[]
	data=[]
	largest_feature_list=[]
	with open(data_train) as data_file:
		for line in data_file:
			line=line.split()
			data.append(line)
	for i in data:
			#line=line.split()
		label.append(int(i[0]))			
		i.pop(0)	
		for j in i:
			j=j.split(":")
			y =int(j[0])-n
			list_data = [0]*(int(y)-1) + [j[1]]
			n=int(j[0])
			list_data = [0]*(int(y)-1) + [j[1]]
			list_data=map(int,list_data)
			feature_data.extend(list_data)
			#print feature_data ,"feature data **********************"
			n=int(j[0])
		n=0
		complete_feature_data.append(feature_data)
		feature_data=[]
	largest_feature_list=max(complete_feature_data,key=len)
	size_largest_list=len(largest_feature_list)
	for i in complete_feature_data:
		if len(i)<size_largest_list:
			i[len(i)+1:size_largest_list]=[0]*(size_largest_list - len(i))
			full_size_data.append(i)
	for i in range(len(full_size_data)):
		full_size_data[i].insert(0,1)
	for i in range(len(full_size_data)):
		full_size_data[i].append(label[i])
	length_data = len(full_size_data)

	return full_size_data,length_data,size_largest_list


def calculate_accuracy_cross_validation(data_test_file,weight):
	false_count =0
	true_count =0
	dot_product=[]
	for i in data_test_file:
		i = [float(j) for j in i ]
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product
		if(-final_product <= 0):
			Predicted_label = 1
				#j+=1
		else:
				#j+=1
			Predicted_label = -1
				#false_count+=1
		if (Predicted_label == i[-1]):
			true_count+=1
		else:
			false_count+=1
			
	accuracy_data=(true_count/float(true_count+false_count))
	return accuracy_data

def calculate_accuracy(weight):
	false_count =0
	true_count =0
	dot_product=[]
	#bias=0
	#j=0
	data_test_file=[]
	data_test_file,length_data,feature_length=read_file(test_data)
	#print feature_length,"------------------------"
	if (len(weight) < feature_length+1):
		weight=weight+[0]*((feature_length+1)-len(weight))
	#	weight = weight
	#print weight,"------------------------------------------------------------"
	for i in data_test_file:
		i = [float(j) for j in i ]
		#print type(weight),type(i[-1]),len(weight),len(i[:-1]),"------------------------------"
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product
		if(-final_product <= 0):
			Predicted_label = 1
				#j+=1
		else:
				#j+=1
			Predicted_label = -1
				#false_count+=1
		if (Predicted_label == i[-1]):
			true_count+=1
		else:
			false_count+=1
			
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
	bias = random.randint(-1,1)
	weight=random.randint(-1,1)
	final_data_initial, data_len, feature_length = read_file(train_data)
	weight_vector = [weight]*(feature_length)
	weight_vector.insert(0,bias)
	weight_vector = [ float(x) for x in weight_vector]
	C_list=[10,50,100,200]
	rate_r_list=[0.50]
	super_list =[]
	#super_super_list =[]
	epoch=[3,5,8]

	log_likelyhood=[]
	for s in range(1):
		
		for sigma_value in C_list:
			updates_final=0
			random.shuffle(final_data_initial)
			for l_rate in rate_r_list:
				for i in epoch:
					for j in range(i):
						for count in range(5):
							test_data,final_data=cross_validation(final_data_initial,data_len,count)
							weight_vector = prediction(final_data,feature_length,bias,weight_vector,l_rate,sigma_value)
							#updates_final = updates_final + updates
							weight_dot=reduce(lambda x,y:x+y,map(lambda x,y:x*y,weight_vector,map(lambda x:x*float(2)/sigma_value, weight_vector)))
							#log=neg_likely+weight_dot
							#log_likelyhood.append(log)
							accuracy =calculate_accuracy_cross_validation(test_data,weight_vector)
							super_list.append([l_rate,sigma_value,format(accuracy*100,'.3f')])
						#super_list = sorted(super_list, key=itemgetter(2),reverse = True)
					#print "rate: ",l_rate,"C: ",c_value, "Accuracy: ",accuracy,"\n"
	#plt.plot(log_likelyhood)
	#plt.ylabel("negativeloglikelihood")
	#plt.xlabel("Epoch")
	#plt.show()
	#print "------------------------------------------------------------------------"					
	#print super_list
	#weight =weight_vector
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
			weight_vector = prediction(final_data_initial,feature_length,bias,weight_vector,super_list[0][0],super_list[0][1])
		accuracy =calculate_accuracy(weight_vector)
		print "-------------------------------------------------"
		print "Accuracy on Test Data is:",accuracy*100," for epoch",i
	
main()