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
submit_file_path = os.path.join(BOP_DATA_PATH, 'submit.txt')
url_query_base = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b42b9e31-44a9-4deb-8bb5-9dd3d2b84898?subscription-key=77f07e1255ed4d0592bb2157cd5d1621&staging=true&timezoneOffset=0&verbose=true&q="

f_w = open(submit_file_path, 'w+')

with open(test_data_path) as f_r:
	for line in f_r:
		parts = line.split('\t')
		questionStr = parts[0]
		answerStr = parts[1]
		question = pseg.lcut(questionStr)
		answer = pseg.lcut(answerStr)

		query_result = urllib.urlopen(url_query_base, urllib.urlencode(questionStr))
		query_result_json = query_result.read().strip()
		intents = []
		total_score = 0

		for intent in query_result_json["intents"]:
			if intent["score"] >= 0.5:
				intents.append(intent["intent"])
		if "询问时间" in intents:
			perc = 1
			score = qtime(answer, perc)
			total_score += score
		if "询问人名" in intents:
			perc = 1
			score = qperson(answer, perc)
			total_score += score
		if "询问数量" in intents:
			perc = 1
			score = qnumber(answer, perc, question)
			total_score += score
		if "询问量度" in intents:
			perc = 1
			score = qenum(answerStr, perc)
			total_score += score
		if "询问名称定义" in intents:
			perc = 1
			score = qdefinition(answer, answerStr, perc, question)
			total_score += score
		if "询问面积" in intents:
			perc = 1
			score = qarea(answer, perc)
			total_score += score
		if "询问方法" in intents:
			perc = 1
			score = qmethod(answer, perc, question)
			total_score += score
		if "询问地点" in intents:
			perc = 1
			score = qlocation(answer, perc)
			total_score += score
		if "询问不同变化" in intents:
			perc = 1
			score = qchange(answerStr, perc)
			total_score += score
		if "询问原因" in intents:
			perc = 1
			score = qreason(answer, perc)
			total_score += score
		if "询问组成" in intents:
			perc = 1
			score = qconsist(answerStr, perc)
			total_score += score
		if "询问属于关系" in intents:
			perc = 1
			score = qpossess(answerStr, perc)
			total_score += score
		if "询问别名" in intents:
			perc = 1
			score = qalias(answerStr, perc)
			total_score += score
		if "询问距离" in intents:
			perc = 1
			score = qdistance(answer, perc)
			total_score += score
		if "询问状态" in intents:
			perc = 1
			score = qstatus(answerStr, perc)
			total_score += score
		if "询问职务" in intents:
			perc = 1
			score = qpost(answer, perc)
			total_score += score
		if "询问模样" in intents:
			perc = 1
			score = qappearance(answerStr, perc)
			total_score += score
		if "询问评价" in intents:
			perc = 1
			score = qeva(answer, perc)
			total_score += score
		if "询问译名" in intents:
			perc = 1
			score = qtranslate(answer, perc, question)
			total_score += score
		if "询问正误" in intents:
			perc = 1
			score = qtorf(answerStr, perc)
			total_score += score
		f_w.write(total_score+'\n')
f_w.close()
		



# foreach line in file:
# 	if line.question == curr_question:
# 		curr_answer_list = jieba.lcut(curr_answer)
# 		socre = 0
# 		for intent in intents: # intents is an array return by LUIS
# 			score += qintent(curr_answer, percentage) # percentage represents how much weight a intent is in the final comparison
# 													  # qintent is the functions in function.py
# 		curr_answer.score = score