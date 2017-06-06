from langdetect import detect
import zhon.pinyin
import re
import urllib
import json

#    nr人名  ns地名  nt機構名  t時間詞  s處所詞  f方位詞  v動詞 a形容詞 m數詞 q量詞
#      0       1        2        3      4        5      6      7    8     9
match = {
    'mreason':  [, , , , , , , , , ],  # 原因
    'mbelong':  [, , , , , , , , , ],  # 归属
    'mdefine':  [, , , , , , , , , ],  # 定义
    'menum':    [, , , , , , , , , ],  # 枚举
    'malias':   [, , , , , , , , , ],  # 别名
    'mmethod':  [, , , , , , , , , ],  # 方法
    'mtime':    [0, 0, 0, 1, 0, 0, 0.2, 0, 1, 0],  # 时间
    'mlocation':[0.5, 1, 0.75, 0.1, 1, 1, 0, 0, 0.2, 0],  # 地点
    'marea':    [0, 0.6, 0.6, 0, 0.6, 0, 0, 0, 1, 1],  # 面积
    'mmeasure': [0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0, 1, 1],  # 量度
    'mperson':  [1, 0.2, 0.2, 0, 0, 0, 0, 0, 0, 0],  # 人名
    'mnumber':  [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # 数量
    'mdistance':[0, 0.7, 0.4, 0, 0.2, 0.2, 0, 0, 0.9, 0.2]  # 距离
    'meva':     [0.2, 0.3, 0.3, 0, 0, 0, 0.2, 1, 0.1, 0.1] #评价
    'mpost':    [0.5, 0.1, 0.5, 0.1, 0, 0, 0.2, 0, 0, 0] #职务
}

wordtype = {
    'nr': 0
    'ns': 1
    'nt': 2
    't': 3
    's': 4
    'f': 5
    'v': 6
    'a': 7
    'm': 8
    'q': 9
}

def ltp_cloud_api(answerStr, pattern):
    url_get_base = "http://api.ltp-cloud.com/analysis/"
    args = { 
        'api_key' : 'u1i1v9Y9555gfxnp4PmKVdhyGcPD7t0xJdklcQCv',
        'text' : answerStr,
        'pattern' : pattern,
        'format' : 'json'
    }
    result = urllib.urlopen(url_get_base, urllib.urlencode(args)) # POST method
    content_json = result.read().strip()
    return content_json

def qtime(answer, perc):
    # answer is the result of jieba.lcut
    # perc is the percentage of current intent from LUIS
    times = [
        '年', '月', '日', '号', '时', '小时', '点', '分', '秒', '天', '岁', '之前', '之后'
    ]
    score = 0
    for word, flag in (answer):
        score += match['mtime'][wordtype[flag]]
        if flag == 't' or word in times:
            score += 0.1
    return score * perc

def qlocation(answer, perc):
    # answer is the result of jieba.lcut
    # perc is the percentage of current intent from LUIS
    score = 0
    for word, flag in (answer):
        score += match['mlocation'][wordtype[flag]]
        if flag == 'ns':
            score += 0.3
    return score * perc

'''
def qarea(answer, perc):
    # answer is the result of jieba.lcut
    # perc is the percentage of current intent from LUIS
    score = 0
    for word, flag in (answer):
        score += match['marea'][wordtype[flag]]
    return score * perc
'''

def qarea(answer, perc):
    area_unit = [
        '平方公里', '公顷', '甲', '英亩', '公母', '坪', '平方公尺', '平方尺', '平方寸', '平方公分',
        '平方米', '平方厘米', '平方毫米', '平方英里'
    ]
    score = 0
    for word, _ in (answer):
        if word == '面积':
            score = 4
    for word, _ in (answer):
        if word in area_unit:
            score += 1  # this one seems better?

def qmeasure(answer, perc):
    # answer is the result of jieba.lcut
    # perc is the percentage of current intent from LUIS
    score = 0
    for word, flag in (answer):
        score += match['mmeasure'][wordtype[flag]]
    return score * perc

def qtranslate(answer, perc, question):
    # question is the result of jieba.lcut(question)
    # answer is the result of jieba.lcut(answer)
    # perc is the percentage of current intent from LUIS
    score = 0
    language = 0
    languages = [
        "af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "fi", "fr", "gu", "he", "hi",
        "hr", "hu", "id", "it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl", "pt", "ro",
        "ru", "sk", "sl", "so", "sq", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi", "zh-cn", "zh-tw"
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
        else:  # detect all other languages
            for aword, _ in (answer):
                if detect(aword) in languages:
                    return 5 * perc

def qperson(answer, perc):
    score = 0
    for word, flag in (answer):
        score += match['mperson'][wordtype[flag]]
        if flag == 'nr' or flag == 'nrfg' or flag == 'nrt':
            score += 0.1
    return score * perc

def qnumber(answer, perc, question):
    qword_count = 0
    score = 0
    for qword, _ in question:
        if qword == '多少' and question[qword_count + 1].word != '?':
            for aword, aflag in answer:
                if aword == question[qword_count + 1].word:
                    score += 0.5
                if aflag == 'm':
                    score += 0.5
        elif qword == '多少' and question[qword_count + 1].word == '?':
            for aword, aflag in answer:
                if aword == question[qword_count - 2].word:  # noun + 是多少？
                    score += 0.5
                if aflag == 'm':
                    score += 0.5
        elif qword == '多' and question[qword_count + 1].word != '少' and question[qword_count + 1].word != '远':  # 多远：距离
            for aword, aflag in answer:
                if aword == question[qword_count + 1].word:
                    score += 0.5
                if aflag == 'm':
                    score += 0.5
        elif qword == '几':
            for aword, aflag in answer:
                if aword == question[qword_count + 1].word:
                    score += 0.5
                if aflag == 'm':
                    score += 0.5

        qword_count += 1
    return score * perc

def qdistance(answer, perc):
    word_count = -1
    distance_unit = [
        '车程', '公里', 'km', '千米', '米', '英尺', '对面', '附近', '不远'
    ]
    for word, flag in (answer):
        word_count += 1
        score = 0
        if word in distance_unit:
            score += 0.5
        if flag == 'm':
            score += 0.5
    return score * perc

def qmethod(answer, perc, question):
    # answer type: array
    # question type: array
    # after getting all the scores, we hv to divide it by the largest score (normalize)
    score = 0
    for qword, qflag in (question):
        for word, flag in (answer):
            if qflag == "n" and flag == "n" and qword == word:
                score += 0.5
            elif qflag == "v" and flag == "v" and qword == word:
                score += 0.5
    return score * perc

def qreason(answerStr, perc):
    # answer type: str
    score = 0
    content_json = ltp_cloud_api(answerStr, 'sdp')

    for content in content_json[0][0]: # reason for these two zero: see sample_return_from_ltp_cloud_api.json
        if "semrelate" in content and content["semrelate"] == "eCau":
            score += 5
            break
        if "semrelate" in content and content["semrelate"] == "eResu":
            score += 5
            break
        if "semrelate" in content and content["semrelate"] == "Reas":
        score += 5
        break
    return score * perc

def qpossess(answerStr, perc):
    score = 0
    content_json = ltp_cloud_api(answerStr, 'sdp')
    
    for content in content_json[0][0]: # reason for these two zero: see sample_return_from_ltp_cloud_api.json
        if "semrelate" in content and content["semrelate"] == "Poss":
            score += 5
            break
        if "semrelate" in content and content["semrelate"] == "Belg":
            score += 5
            break
    return score * perc

def qdefinition(answer, answerStr, perc, question):
    score = 0
    if "网址" in answerStr:
        if urls = re.findall('(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', answerStr):
            score += 3
    elif "是" in answerStr or "指" in answerStr or "叫" in answerStr or "哪" in answerStr:
        content_json = ltp_cloud_api(answerStr, 'sdp')
        for content in content_json[0][0]: # reason for these two zero: see sample_return_from_ltp_cloud_api.json
            if "semrelate" in content and content["semrelate"] == "Clas":
                score += 5
                break
    elif "什么" in answerStr:
        word_count = -1
        for qword, _ in (question):
            word_count += 1
            if qword == "什么":
                for aword, _ in (answer):
                    if aword == question[word_count + 1].word:
                        score += 3
                        break
    else:
        score += 0
    return score * perc

def qeva(answer, perc):
    score = 0
    for word, flag in (answer):
        score += match['meva'][wordtype[flag]]
    return score * perc

def qalias(answerStr, perc):
    score = 0
    aliass = [
        "又叫", "还叫", "又称", "简称", "别称", "原来", "原名", "名为",
        "叫", "全称", "名称", "称为", "称作", "前身"
    ]
    for alias in (aliass):
        if alias in answerStr:
            score += 5
    return score * perc

def qpost(answer, perc):
    score = 0
    for word, flag in (answer):
        score += match['mpost'][wordtype[flag]]
    return score * perc


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
