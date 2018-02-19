python 3_4_no_shuffle.py 1 a5a.train a5a.train >output_non_shuffled_train.txt
python 3_4_no_shuffle.py 1 a5a.train a5a.test > output_non_shuffled_test.txt
python 3_4_shuffle.py 1 a5a.train a5a.train > output_shuffled_train.txt
python 3_4_shuffle.py 1 a5a.train a5a.test > output_shuffled_test.txt

