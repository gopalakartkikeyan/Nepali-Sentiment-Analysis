import pandas as pd
import math as mth
from functools import reduce
from collections import Counter 
import numpy as np
from sklearn.naive_bayes import GaussianNB
import pickle
import datetime
import random
import sys
from sklearn import metrics
import collections

now = str(datetime.datetime.now())

df = pd.read_csv('merge.csv', delimiter=',', names=['Data', 'Label']);
# print(df)
first_col = df.ix[1:, 0]
# print(first_row)
second_col = df.ix[1:, 1]
# print(second_row)
data_with_split = []
each_docs = []
stop_words_split_final = []

def split_doc():
    for data in first_col:
        each_line = data.split()
        data_with_split.append(each_line)
    return data_with_split  # it returns arr of each docs with spleted words


word_arrays = []
word_arrays = split_doc()
length_of_docs = len(word_arrays)
print(word_arrays)

def individual_words():
    my_set = set.union(*map(set, word_arrays))  # seperate each individual words from data to make matrix
    return my_set


def set_to_list():
    my_set_list = individual_words()
    convert_into_list = list(my_set_list)
    return convert_into_list


individual_word_array = set_to_list()


def count_occurence_of_word_vocab():
    my_set = individual_words()
    doc = {}
    word_dict = {}
    for i in range(len(word_arrays)):
        for word in word_arrays[i]:
            word_dict = dict.fromkeys(my_set, 0)

    for count_word_value in word_arrays:
        for word in count_word_value:
            if word in word_dict:
                word_dict[word] += 1
    return word_dict


word_dict = count_occurence_of_word_vocab()
print(len(word_dict))


length_word_dict = len(word_dict)

def vectorizer_docs(line):
    vectorizer_docs = []
    matrix_doc = []
    for word in individual_word_array:
        if word in line:
            vectorizer_docs.append(1)
        else:
            vectorizer_docs.append(0)
    return vectorizer_docs
    vectorizer_docs.clear()


doc_vec1 = []
doc_vec2 = []
for line in word_arrays:
    doc_vec1 = vectorizer_docs(line)
    doc_vec2.append(doc_vec1)
# print(doc_vec2)


def computeTf(docs_list):
    tf_vec = []
    tf_each_doc_vec = []
    doc_word_count = len(docs_list)
    count_each_word = Counter(docs_list)  # counter count the word in list how many times it occure
    for each_word,val in word_dict.items():
        if each_word in docs_list:
            count = count_each_word.get(each_word)
            tf_vec.append(count / float(doc_word_count))
        else:
            tf_vec.append(0)
    tf_each_doc_vec.append(tf_vec)
    return tf_each_doc_vec


tf = []
tf_vec = []
for each_line in word_arrays:
    tf = computeTf(each_line)
    tf_vec += tf
# print("Term Frequency")
# print(tf_vec)

countIdfforwordvalue = {}
word_dict = count_occurence_of_word_vocab()
my_set = individual_words()


def computeCountDict(word_dict, word_arrays):
    countIdfforword = {}
    for i in range(1, len(my_set)):
        countIdfforword = dict.fromkeys(my_set, 0)
    for word, value in word_dict.items():
        for each_line_item in word_arrays:
            if word in each_line_item:
                countIdfforword[word] += 1
        # else:
        # 	countIdfforword[word] = 1
    return countIdfforword


countIdfforwordvalue = computeCountDict(word_dict, word_arrays)





def computeIdf(docs_list):
    idf_vec = []
    idf_each_doc_vec = []
    for each_word,val in word_dict.items():
        if each_word in docs_list:
            word_value_in_each_doc = countIdfforwordvalue.get(each_word)
            idf_vec.append(mth.log(length_of_docs / word_value_in_each_doc))
        else:
            idf_vec.append(0)
    idf_each_doc_vec.append(idf_vec)
    return idf_each_doc_vec


idf = []
idf_vec = []
for each_line in word_arrays:
    idf = computeIdf(each_line)
    idf_vec += idf


compute_TfIdf_vec = []


def compute_TfIdf(Tfvec, Idfvec):
    compute_TfIdf_vec = [a * b for a, b in zip(Tfvec, Idfvec)]
    return compute_TfIdf_vec


compute_TfIdf_vector_for_each_docs = []
compute_TfIdf_vector_collection = []
for tf_list, idf_list in zip(tf_vec, idf_vec):  # zip helps to iteration two different collection samultaneously
    compute_TfIdf_vector_for_each_docs = compute_TfIdf(tf_list, idf_list)
    compute_TfIdf_vector_collection.append(compute_TfIdf_vector_for_each_docs)
# make model with sk-learn

features = np.array(compute_TfIdf_vector_collection)
labels_string = np.array(second_col)


labels_list = [int(int_labels) for int_labels in labels_string]
labels = np.array(labels_list)


array_length = len(features)
# print(type(features))

features_taken_len = int(array_length * 92 / 100)  # 80% of data make for train 20% remening data for testing
feature_array_train = features[:features_taken_len]  # 80% of data make for train 20% remening data for testing
labels_array_train = labels[:features_taken_len]
feature_array_test = features[features_taken_len:]  # 80% of data make for train 20% remening data for testing
labels_array_test =  labels[features_taken_len:]

naive_byes = GaussianNB()  # create  object  from  GaussianNb  class
TrainData = naive_byes.fit(feature_array_train, labels_array_train)

classifier_data = open("classify_data.pickle", "wb")
pickle.dump(TrainData, classifier_data)
classifier_data.close()


with open('classify_data.pickle', 'rb') as pickle_saved_data:
    unpickled_data = pickle.load(pickle_saved_data)



predict_result = unpickled_data.predict(feature_array_test)
print("predict")
print(predict_result)




precision = metrics.precision_score(predict_result,labels_array_test ,average='weighted')
print("precision")
print(precision)


recall = metrics.recall_score(predict_result,labels_array_test,average='weighted')
print("recall")
print(recall)



f_score = 2*(precision*recall)/(precision+recall)
print("f_score")
print(f_score)


#
# #prediction after taking input from user
print("***************************************")
input_data = input("Type Text For Prediction ")
each_input_word = []
# change into array of word
each_input_word = input_data.split()

#input data from user
length_input_data = len(each_input_word)

count_each_inputword = Counter(each_input_word)
input_data_tfvec = []
# tf_each_input_word = []
#TF computation of input data

for word,val in word_dict.items():#where word_dict is all the word collection from data set
    if word in each_input_word:
        count = count_each_inputword.get(word)
        input_data_tfvec.append(count / float(length_input_data))
    else:
        input_data_tfvec.append(0)
# to make predict input value similar as our training sample we use reshape
value_for_predict = np.array(input_data_tfvec).reshape(1,-1)
predict = unpickled_data.predict(value_for_predict)
print(predict)
