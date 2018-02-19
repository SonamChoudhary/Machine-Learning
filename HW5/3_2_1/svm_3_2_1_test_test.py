import sys
import random
import demo_treesvm_tran_test

#train_data =  sys.argv[1]
label_data = sys.argv[1]
#test_data =  sys.argv[2]
test_label = sys.argv[2]


def learning_rate(t,r,c):
	rate_t= r/float(1+(r*t/c))
	return rate_t

def svm_prediction(final_data,feature_length,bias,weight,rate_r,C):
	#print final_data[:4],"-------------"
	#print bias,"---",rate,"----",weight
	false_count =0
	true_count =0
	dot_product=[]
	#final_product=[]
	t_count =0
	for i in final_data:
		t_count+=1
		rate=learning_rate(t_count,rate_r,C)
		#i = [float(j) for j in i]
		temp=[]
		for val in i:
			if type(i)==type(3.33):
				temp.append(float(val))
			else:
				temp.append(float(-1))

		i=temp
		#print type(i[:-1]) ,"-----",type(weight),"----------",i[:-1],"---------------weight-------------",weight
		#print weight,"-----------------",i[:-1]
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		#print dot_product,"----------------"
		final_product = reduce(lambda x,y:x+y ,dot_product)
		#print final_product
		#print type(final_product) , "----------",type(dot_product) ,"------", type(bias)
		derived_label = final_product
		if(derived_label*i[-1] <= 1):
			product=map(lambda x: x*i[-1]*rate*C,i[:-1])
			weight_r = map(lambda x: x*(1-rate), weight)
			#print type((1-rate)),type(weight),"*********************************************"
			weight=map(lambda x,y:x+y ,weight_r,product)
			#bias =bias + float(rate*i[-1])
			false_count+=1
		else:
			#weight = (1-rate)*weight			
			weight = map(lambda x: x*(1-rate), weight)
			true_count+=1
		#t_count+=1
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
	#print feature_length,"************256************"
	#final_data = zip(data,label)
	for i in range(length_data):
		data[i].append(label[i][-1])
	return data,length_data,feature_length
	#for i in range(length_data):
		#final_data.append(data[i],label[i])

	#print final_data[:3]

	#print data[:3]+ label[:3]
def calculate_accuracy(final_data,weight,bias):
	false_count =0
	true_count =0
	dot_product=[]
	#bias=1
	#j=0
	#for i in final_data:
	#	print len(i),"            ----tree test data"
	data_test_file=[]
	#data_test_file,length_data,feature_length=read_file(test_data,test_label)
	#for i in data_test_file:
	for i in final_data:
		#print len(i),"--------------------------------------------"
		#i =[float(j) for j in i]
		temp=[]
		for val in i:
			if type(i)==type(3.33):
				temp.append(float(val))
			else:
				temp.append(float(-1))

		i=temp
		#print type(weight),"---------------------",weight,"----------------",type(i[:-1])
		try:
			dot_product = map(lambda x,y:x*y,weight,i[:-1])
		except Exception:
			pass
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product
		if(derived_label*i[-1] > 0):
			true_count+=1
			#j= j+1
		else:
			#j+=1
			false_count+=1
	print "No of mistakes on Test data: ",false_count
	accuracy_data=(true_count/float(true_count+false_count))
	return accuracy_data

def read_file_dtree(final_data,label_data_f):
	label=[]
	with open(label_data_f) as label_file:
		for line in label_file:
				line = line.split()
				label.append(line)
	length_data = len(final_data)
	feature_length = len(final_data[0])
	for i in range(length_data):
		final_data[i].append(label[i][-1])

	return final_data,feature_length

def main():
	bias = 0
	C=0.5
	r=0.01
	label=[]
	label_test=[]
	final_data_train,final_data_test = demo_treesvm_tran_test.main()
	#print final_data_train[:10]
	#print len(final_data_test),"---",len(final_data_test[0])
	
	with open(test_label) as label_file:
		for line in label_file:
				line = line.split()
				label_test.append(line)
	#length_data_test = len(final_data)
	#feature_length = len(final_data[0])
	for i in range(len(final_data_test)):
		final_data_test[i].append(label_test[i][-1])

	#print final_data_test[:5] ,"test---------------------"
	#print len(final_data_test[0]),"*******************************************"
	#final_data, data_len, feature_length = read_file(train_data,label_data)"""
	"""feature_length=f_length+1
	for i in final_data:
		i.insert(0,bias)
	print len(i),"----------",i"""
	"""length_data = len(final_data_train)
	feature_length = len(final_data_train[0])
	for i in range(length_data):
		final_data_train[i].append(label[i][-1])"""

	final_data,feature_length =read_file_dtree(final_data_train,label_data)
	weight_vector = [0]*(feature_length-1)
	weight_vector.insert(0,bias)
	weight_vector = [ float(x) for x in weight_vector]
	#print len(weight_vector),"----------------------",weight_vector
	#print weight_vector
	#final_data_test_acc,feature_length_test = read_file_dtree(final_data_test,test_label)
	epoch=[3,5,8]
	for i in epoch:
		for j in range(i):
			updates_final=0
			random.shuffle(final_data)
			#rate=learning_rate(j,r,C)
			weight_vector, updates =svm_prediction(final_data,feature_length,bias,weight_vector,r,C)
			updates_final = updates_final + updates
		#print "Weight Vector:",weight_vector
		#print "Total no of updates :", updates_final 
		#accuracy =calculate_accuracy(final_data,weight_vector,bias)
		#print "Accuracy on Testing with training data is:",accuracy*100," for epoch",i
		#for i in final_data:
		#	print len(i),"            ----tree test data"
		accuracy =calculate_accuracy(final_data_test,weight_vector,bias)
		print "Accuracy on Testing with Testing data is:",accuracy*100," for epoch",i


main()