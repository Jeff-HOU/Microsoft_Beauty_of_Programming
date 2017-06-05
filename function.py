from langdetect import detect
import zhon.pinyin
import re

#    nr人名  ns地名  nt機構名  t時間詞  s處所詞  f方位詞  v動詞 a形容詞 m數詞 q量詞
#      0       1        2        3      4        5      6      7    8     9
match = {
	'mreason':  [,,,,,,,,,],#原因
	'mbelong':  [,,,,,,,,,],#归属
	'mdefine':  [,,,,,,,,,],#定义
	'menum':    [,,,,,,,,,],#枚举
	'malias':   [,,,,,,,,,],#别名
	'mmethod':  [,,,,,,,,,],#方法
	'mtime':    [0,0,0,1,0,0,0.2,0,1,0],#时间
	'mlocation':[0.5,1,0.75,0.1,1,1,0,0,0.2,0],#地点
	'marea':    [0,0.6,0.6,0,0.6,0,0,0,1,1],#面积
	'mmeasure': [0.5,0.5,0.5,0.5,0,0,0,0,1,1],#量度
	'mperson':  [1,0.2,0.2,0,0,0,0,0,0,0],#人名
	'marea':    [,,,,,,,,,]#面积
}

wordtype = {
	'nr': 0
	'ns': 1
	'nt': 2
	't' : 3
	's' : 4
	'f' : 5
	'v' : 6
	'a' : 7
	'm' : 8
	'q' : 9
}




def qtime(answer, perc):
	# answer is the result of jieba.lcut
	# perc is the percentage of current intent from LUIS
	score = 0
	for word, flag in (answer):
		score += match['mtime'][wordtype[flag]]
	return score * perc

def qlocation(answer, perc):
	# answer is the result of jieba.lcut
	# perc is the percentage of current intent from LUIS
	score = 0
	for word, flag in (answer):
		score += match['mlocation'][wordtype[flag]]
	return score * perc

def qarea(answer, perc):
	# answer is the result of jieba.lcut
	# perc is the percentage of current intent from LUIS
	score = 0
	for word, flag in (answer):
		score += match['marea'][wordtype[flag]]
	return score * perc

def qmeasure(answer, perc):
	# answer is the result of jieba.lcut
	# perc is the percentage of current intent from LUIS
	score = 0
	for word, flag in (answer):
		score += match['mmeasure'][wordtype[flag]]
	return score * perc

def qalias(answer, perc, question):
	# question is the result of jieba.lcut(question)
	# answer is the result of jieba.lcut(answer)
	# perc is the percentage of current intent from LUIS
	score = 0
	language = 0
	languages = [
		"af","ar","bg","bn","ca","cs","cy","da","de","el","en","es","et","fa","fi","fr","gu","he","hi",
		"hr","hu","id","it","ja","kn","ko","lt","lv","mk","ml","mr","ne","nl","no","pa","pl","pt","ro",
		"ru","sk","sl","so","sq","sv","sw","ta","te","th","tl","tr","uk","ur","vi","zh-cn","zh-tw"
	]
	'''
	languages = [
		"南非荷兰语": "af","": "ar","": "bg","": "bn","": "ca","": "cs",
		"": "cy","": "da","": "de","": "el","": "en","": "es","": "et",
		"": "fa","": "fi","": "fr","": "gu","": "he","": "hi","": "hr",
		"": "hu","": "id","": "it","": "ja","": "kn","": "ko","": "lt",
		"": "lv","": "mk","": "ml","": "mr","": "ne","": "nl","": "no",
		"": "pa","": "pl","": "pt","": "ro","": "ru","": "sk","": "sl",
		"": "so","": "sq","": "sv","": "sw","": "ta","": "te","": "th",
		"": "tl","": "tr","": "uk","": "ur","": "vi","": "zh-cn","": "zh-tw",
		"": "af","": "ar","": "bg","": "bn","": "ca","": "cs",
		"": "cy","": "da","": "de","": "el","": "en","": "es","": "et",
		"": "fa","": "fi","": "fr","": "gu","": "he","": "hi","": "hr","": "hu",
		"": "id","": "it","": "ja","": "kn","": "ko","": "lt","": "lv",
		"": "mk","": "ml","": "mr","": "ne","": "nl","": "no","": "pa",
		"": "pl","": "pt","": "ro","": "ru","": "sk","": "sl","": "so",
		"": "sq","": "sv","": "sw","": "ta","": "te","": "th","": "tl",
		"": "tr","": "uk","": "ur","": "vi","": "zh-cn","": "zh-tw"
	]
	'''
	for qword, _ in (question):
		if qword == '英语' or qword == '英文':
			for aword, _ in (answer):
				if detect(aword) == 'en':
					return 5 * perc
			return 0
		elif qword == '拼音':
			for aword, _ in (answer):
				if not re.findall(zhon.pinyin.word, aword, re.I):
					return 5 * perc
		else: # detect all other languages
			for aword, _ in (answer):
				if detect(aword) in languages:
					return 5 * perc

def qperson(answer, perc):
	score = 0
	for word, flag in (answer):
		score += match['mperson'][wordtype[flag]]
	return score * perc

def qarea(answer, perc):
	area_unit = [
		'平方公里','公顷','甲‘英亩','公母','坪','平方公尺','平方尺','平方寸','平方公分'，

	]
	score = 0
	for word, _ in (answer):
		if word == '面积':
			score = 4
	for word, _ in (answer):
		if word in area_unit:
			score


'''
#nr人名  ns地名  nt機構名  t時間詞  s處所詞  f方位詞  v動詞 a形容詞 m數詞 q量詞
#  0       1        2        3      4        5      6      7    8     9
[
	[,,,,,,,,,],#原因
	[,,,,,,,,,],#归属 
	[,,,,,,,,,],#定义
	[,,,,,,,,,],#枚举
	[,,,,,,,,,],#别名
	[,,,,,,,,,],#方法
	[,,,,,,,,,],#时间
	[,,,,,,,,,],#地点
	[,,,,,,,,,],#面积
]
'''