# general control
import function
import luis_control
import jieba
import jieba.posseg as pseg
import os
import json
#import sys

jieba.initialize()
#jieba.load_userdict('dict/v19.1')
#jieba.load_userdict('dict/temporalNoun')
jieba.enable_parallel(8)
BOP_DATA_PATH = './BoP2017_DBAQ_dev_train_data'
train_data_path = os.path.join(BOP_DATA_PATH, 'BoP2017-DBQA.train.txt')
dev_data_path = os.path.join(BOP_DATA_PATH, 'BoP2017-DBQA.dev.txt')
test_data_path = os.path.join(BOP_DATA_PATH, 'BoP2017-DBQA.test.txt')
ltp_url_get_base = "http://api.ltp-cloud.com/analysis/"
ltp_args = {}



# foreach line in file:
# 	if line.question == curr_question:
# 		curr_answer_list = jieba.lcut(curr_answer)
# 		socre = 0
# 		for intent in intents: # intents is an array return by LUIS
# 			score += qintent(curr_answer, percentage) # percentage represents how much weight a intent is in the final comparison
# 													  # qintent is the functions in function.py
# 		curr_answer.score = score