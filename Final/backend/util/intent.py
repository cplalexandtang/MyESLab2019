import random

# GREETINGS
GREETINGS = ["妳好", "你好", "哈囉", "嗨", "安安", "Hello", "Hi", "hello", "hi"]
THANK = ["感恩", "感謝", "謝謝", "thanks", "Thanks", "THANKS"]

# CONFIRM/NEGATION
YES = ["要", "是", "對", "好", "願意", "ok", "OK", "Ok", "會"]
NO = ["不"]
I_WANT = ["我要"]
I_DONT_WANT = ["我不要"]
WANT = ["想要","要","想"]
DISLIKE = ["不喜歡","討厭",]

# ASK
ASK = ["嗎?", "阿?", "啊?", "嗎", "啊", "阿"]
HOW = ["怎麼","怎麼辦","如何"]
WHY = ["為甚麼呢?", "為什麼", "why", "Why", "WHY", "為甚麼阿", "為啥", "啥", "為何"]

# HAVE
HAVE = ["有"]
REPLY_HAVE = ["有啊哈哈哈", "幹嘛突然問這個啦><", "這是好問題耶", "小夏沒想過這個問題耶QQ"]

# NAME
NAME = ["小夏"]
REPLY_NAME = ["什麼事><", "不要一直叫人家的名子啦嗚嗚", "被呼喚了好開心嘻嘻"]

# COMMON NOUMS

# COMMON VERBS

# COMMON ADJ
OLD = ["幾歲", "你幾歲", "妳幾歲", "歲", "年紀", "貴庚", "年齡"]
ADJ = ["長", "短", "遠", "近", "乖", "涼", "冰", "燙", "帥", "美", "漂亮", "正", "餓", "累", "猛", "厲害", "高", "矮", "胖", "瘦", "年輕", "老", "有趣", "無聊", "好玩", "冷" ,"熱"]

# REPLYS
LOVE_YOU = ["愛你", "最愛你", "最喜歡你", "喜歡你", "超愛你"]
WELCOME = ["不客氣", "OK的"]
BYE = ["掰掰", "再見", "拜拜", "Bye", "bye", "先洗澡喔"]
GOOD = ["很棒", "很強", "超棒", "棒", "讚", "超讚", "很讚"]
KNOW = ["知道", "了解", "懂"]

# DOT
DOT = ["好棒喔哈哈", "歐歐~", "喔喔~", "河河河", "噢~", "是喔", "哈哈哈", "真假", "哈哈 我先洗澡喔 等下回"]

# DIRTY
DIRTY_WORD = ["媽的", "馬的", "幹你娘", "幹妳娘", "操你", "操妳", "Fuck", "fuck", "Shit", "shit"]
REPLY_DIRTY = ["老師有教你不能罵髒話嗎?", "罵髒話是不好的行為噢!不乖!", "不乖", "不要亂教我啦!", "去罰站", "提水桶罰站", "都罵小夏嗚嗚 森七七耶"]

def contains(WORD_LIST, msg):
	for word in WORD_LIST:
		if word in msg:
			return True
	return False

def parse(msg):
	if "位置資訊" in msg:
		return "可以看一下使用說明的影片哦~"

	# S + V.
	# S + have.
	if contains(HAVE, msg) == True:
		if contains(["男朋友", "男友", "交往", "戀愛"], msg) == True:
			return random.choice(["當然有啊><我們在一起好久了", "問這個小夏會害羞啦><", "跟你講的話要幫小夏保密喔><"])
		if contains(ASK, msg) == True:
			return random.choice(REPLY_HAVE)
		return random.choice(DOT)

	# S + be.
	# S + adj.
	if contains(["慢"], msg) == True:
		return "慢工出細活，等等我！"
	if contains(OLD, msg) == True:
		return "小夏今年剛出生 還沒滿一歲喔><"
	if contains(ADJ, msg) == True:
		if contains(ASK, msg) == True:
			return random.choice(["小夏又沒看過你 好難回答喔QQ", "小夏怎麼會知道嗚嗚", "好問題耶哈哈"])
		return random.choice(GOOD) 

	if contains(DIRTY_WORD, msg) == True or msg == "幹":
		return random.choice(REPLY_DIRTY)
	if contains(GREETINGS, msg) == True:
		return random.choice(GREETINGS)
	if contains(BYE, msg) == True:
		return random.choice(BYE)
	if contains(THANK, msg) == True:
		return random.choice(WELCOME)
	if contains(NAME, msg) == True:
		return random.choice(REPLY_NAME)

	return "你剛剛是說" + str(msg) + "對吧~\n可是對不起我還沒學好怎麼講話...不過你可以試試看輸入「說明」來認識小夏喔!"