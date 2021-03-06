#Machine_Learning_HW_2
import sys
import random
margin = sys.argv[1]
train =  sys.argv[2]
test = sys.argv[3]
def perceptron_prediction(weight,input_data,label,rate,bias_new):
	bias = bias_new
	false_count =0
	true_count =0
	dot_product=[]
	j=0
	for i in input_data:
		dot_product = map(lambda x,y:x*y,weight,i)
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product + bias
		if(derived_label*label[j] <= float(margin)):
			product=map(lambda x: x*label[j]*rate,i)
			weight=map(lambda x,y:x+y ,weight,product)
			bias =bias + float(rate*label[j])
			false_count+=1
			j+=1
		else:
			true_count+=1
			j+=1		
	return weight ,false_count

def create_weight_vector(list_size,train_data,label,rate,weight,bias_new):
	bias=bias_new
	learning_rate = rate
	weight_vector =	weight
	weight_final=[]
	full_size_data=[]
	for i in train_data:
		if len(i)<list_size:
			i[len(i)+1:list_size]=[0]*(list_size - len(i))
		full_size_data.append(i)
	weight_final , updates =perceptron_prediction(weight_vector,full_size_data,label,learning_rate,bias)
	return weight_final,updates


def read_file(data):
		epoch=1
		weight_final=[]
		label = []
		feature_data=[]
		complete_feature_data =[]
		n=0
		list_data=[]
		largest_feature_list=[]			
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
				n=int(j[0])
			n=0
			complete_feature_data.append(feature_data)
			feature_data=[]
		largest_feature_list=max(complete_feature_data,key=len)
		size_largest_list=len(largest_feature_list)		
		return size_largest_list,complete_feature_data,label

def calculate_accuracy(weight_vector):
	weight_final=[]
	label = []
	feature_data=[]
	complete_feature_data =[]
	n=0
	data=[]
	list_data=[]
	largest_feature_list=[]
	false_count =0
	true_count =0
	dot_product=[]
	j=0
	bias=0
	full_size_data=[]
	with open(test) as data_file:
		for line in data_file:
				line=line.split()
				data.append(line)
		largest_list_size,complete_data,label=read_file(data)
		if len(weight_vector) < largest_list_size:
			weight_vector=weight_vector+[0]*(largest_list_size-len(weight_vector))
		for i in complete_data:
			if len(i)<largest_list_size:
				i[len(i)+1:largest_list_size]=[0]*(largest_list_size - len(i))
			full_size_data.append(i)
			dot_product = map(lambda x,y:x*y,weight_vector,i)
			final_product = reduce(lambda x,y:x+y ,dot_product)
			derived_label = final_product+bias
			if(derived_label*label[j] > 0):
				true_count+=1
				j+=1
			else:
				j+=1
				false_count+=1
		print "No of mistakes on Test data: ",false_count
		accuracy_data=(true_count/float(true_count+false_count))
	return accuracy_data

def main():
	print "\n********************Simple Perceptron shuffle epoch**************\n"
	weight=random.randint(-2,2)
	weight_vector=[]
	data=[]
	complete_data=[]
	label=[]
	rate =0
	bias = random.randint(-2,2)
	print bias," *****************bias_random*****************" 
	epoch=[3,5]
	learning_rate=[1,0.1,0.01,0.001]
	for rate in learning_rate:
		for i in epoch:
			updates_final=0
			for j in range(i):	
				data=[]
				with open(train) as data_file:
					for line in data_file:
						line=line.split()
						data.append(line)
				random.shuffle(data)
				largest_list_size,complete_data,label=read_file(data)
				if j==0:
					weight_vector = [weight]*largest_list_size
				#print weight_vector	
				weight_vector,updates=create_weight_vector(largest_list_size,complete_data,label,rate,weight_vector,bias)
				#print updates
				#print "weight vector :",weight_vector
				updates_final = updates_final + updates
			#print weight_vector	
			print "Learning rate :",rate	
			print "Total no of updates :", updates_final 
			accuracy=calculate_accuracy(weight_vector)
			print "Accuracy on Test Data is:",accuracy*100," for epoch",i 
			print "\n","\n"

main()	








