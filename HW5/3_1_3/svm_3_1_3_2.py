import sys
import random
train_data =  sys.argv[1]
label_data = sys.argv[2]
test_data =  sys.argv[3]
test_label = sys.argv[4]


def learning_rate(t,r,c):
	rate_t= r/float(1+(r*t/c))
	return rate_t

def cal_precision_recall_f(true_positive,false_positive,false_negative):
	#print true_positive,false_positive,false_negative ,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	precision = true_positive/float(true_positive+false_positive)
	recall = true_positive/float(true_positive+false_negative)
	F_value = 2*((precision*recall)/float(precision+recall))
	return precision,recall,F_value	

def svm_prediction(final_data,feature_length,bias,weight,rate_r,C):
	#print final_data[:4],"-------------"
	#print bias,"---",rate,"----",weight
	false_count =0
	true_count =0
	dot_product=[]
	t_count = 0
	#final_product=[]
	for i in final_data:
		t_count+=1
		rate=learning_rate(t_count,rate_r,C)
		i = [float(j) for j in i ]
		#print type(i[-1]) ,"-----",type(weight[0])
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
def calculate_accuracy(weight):
	false_count =0
	true_count =0
	dot_product=[]
	true_positive =0
	false_positive = 0
	false_negative =0
	#bias=1
	#j=0
	data_test_file=[]
	data_test_file,length_data,feature_length=read_file(test_data,test_label)
	for i in data_test_file:
		i = [float(j) for j in i ]
		dot_product = map(lambda x,y:x*y,weight,i[:-1])
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product
		#print type(derived_label) ,derived_label ,type(i[-1]),i[-1],"------------"
		if (derived_label > 0 and i[-1] > 0):
			true_positive += 1
		elif (derived_label >0 and i[-1] < 0):
			false_positive+=1
		elif(derived_label < 0  and i[-1] > 0):
			false_negative += 1
		if(derived_label*i[-1] > 0):
			true_count+=1
			#j= j+1
		else:
			#j+=1
			false_count+=1

	print "True Count:",true_count," False count:",false_count
	print "TP:",true_positive," FP:",false_positive," f_1:",false_negative
	accuracy_data=(true_count/float(true_count+false_count))
	precision,recall,F_value=cal_precision_recall_f(true_positive,false_positive,false_negative)
	return accuracy_data ,precision,recall,F_value
	

def main():
	bias = 0
	C=1
	r=0.01
	final_data, data_len, feature_length = read_file(train_data,label_data)
	weight_vector = [0]*(feature_length-1)
	weight_vector.insert(0,bias)
	weight_vector = [ float(x) for x in weight_vector]
	#print len(weight_vector),"----------------------",weight_vector
	#print weight_vector
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
		accuracy,precision,recall,F_value =calculate_accuracy(weight_vector)
		print "Accuracy on Test Data is:",accuracy*100," for epoch",i
		print "Precision:",precision," Recall:",recall ," F_value:",F_value ,"\n"
		print "-------------------------------------------------------------------"


main()