#Machine_Learning_HW_2
import random
def perceptron_prediction(weight,input_data,label,rate):
	margin = 0
	bias =0
	false_count =0
	true_count =0
	dot_product=[]
	j=0
	for i in input_data:
		dot_product = map(lambda x,y:x*y,weight,i)
		final_product = reduce(lambda x,y:x+y ,dot_product)
		derived_label = final_product+bias
		if(derived_label*label[j]<= margin):
			product=map(lambda x: x*label[j]*rate,i)
			weight=map(lambda x,y:x+y ,weight,product)
			bias =bias + float(rate*label[j])
			false_count+=1
			j+=1
		else:
			true_count+=1
			j+=1
	print "No of mistakes on training data:" , false_count
	accuracy_data=(true_count/float(true_count+false_count))
	#print "Accuracy on Training data :",accuracy_data*100
	print "Margin :",margin	
	print "Learning rate :", rate			
	return weight

def create_weight_vector(list_size,train_data,label):
	learning_rate = 1
	weight_vector=[]
	weight_final=[]
	weight_vector =[0]*list_size
	full_size_data=[]
	for i in train_data:
		if len(i)<list_size:
			i[len(i)+1:list_size]=[0]*(list_size - len(i))
		full_size_data.append(i)
	weight_final =perceptron_prediction(weight_vector,full_size_data,label,learning_rate)
	return weight_final


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

def main():
	weight_vector=[]
	data=[]
	complete_data=[]
	label=[]
	with open("table2") as data_file:
		for line in data_file:
			line=line.split()
			data.append(line)
	largest_list_size,complete_data,label=read_file(data)
	weight_vector=create_weight_vector(largest_list_size,complete_data,label)
	print "weight vector :",weight_vector

main()	



