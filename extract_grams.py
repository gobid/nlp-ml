import os
import time
import MySQLdb

class Tree(object):
    def __init__(self):
        self.children = []
        self.data = None

def num_open_paren(str):
	return str.count("(")

def num_closed_paren(str):
	return str.count(")")

def strip_ends(str):
	return str[1:len(str)-1]

def create_tree(str): 
	tree = Tree()
	# base case
	if num_open_paren(str) == 1 and num_closed_paren(str) == 1:
		tree.data = strip_ends(str).split()[1]
		return tree
	# other case 
	str = strip_ends(str)
	first_space = str.find(" ")
	str = str[first_space+1:len(str)] # remove first word i.e. remove VBZ
	paren_cnt = 0
	curr = 0
	start = 0
	for c in str:
		if c == '(':
			paren_cnt += 1
		if c == ')':
			paren_cnt -= 1
			if paren_cnt == 0:
				substring = str[start:curr+1]
				tree.children.append(create_tree(substring))
				start = curr + 1
		curr += 1
	return tree

def formList(tree):
	word_list = []
	# base case
	if len(tree.children) == 0:
		word_list.append(tree.data)
	for child in tree.children:
		word_list += formList(child)
	return word_list

def findDepthHelper(tree, str_arr, depth):
	depth_possibilities = []
	tree_list = formList(tree)
	if set(str_arr).issubset(set(tree_list)):
		depth_possibilities.append(depth)
		depth += 1
		for child in tree.children:
			depth_possibilities += findDepthHelper(child, str_arr, depth)
		depth -= 1
	return depth_possibilities	

def findDepth(tree, str): 
	str_arr = str.split()
	depth_possibilities = findDepthHelper(tree, str_arr, 0)
	if (len(depth_possibilities) == 0): return 0 
	return max(depth_possibilities) 

def get_depth(tree):
	if len(tree.children) == 0:
		return 0
	depths = []
	for child in tree.children:
		depths.append(1 + get_depth(child))
	return max(depths)

def parse(sentence):
	os.popen("echo '" + sentence + "' > ~/app/stanfordtemp.txt")
	parser_out = os.popen("~/app/stanford-parser-2012-11-12/lexparser.sh ~/app/stanfordtemp.txt").readlines()
	bracketed_parse = " ".join( [i.strip() for i in parser_out if len(i.strip()) > 0 and i.strip()[0] == "("] )
	return bracketed_parse

def modifierPercentage(str, parse): # consider the list of parts of speech
	return float(parse.count("JJ") + parse.count("RB"))/len(str.split())

def bitVector(example, top_unigrams, top_bigrams, top_trigrams):
	prs = parse(example)
	
	ms = prs.split(") (ROOT ")
	ms[0] = ms[0][6:] # remove root at beginnning
	
	ms_size = len(ms) 
	last_ind = ms_size - 1
	ms[last_ind] = ms[last_ind][:-1] # remove extra paren at end
	
	trees = []
	for s in ms:
		trees.append(create_tree(s))

	bit_vector = []
	for i in range(0, len(top_unigrams)):
		if top_unigrams[i] in example: 
			poss_depths = []
			for tree in trees:
				poss_depths.append(findDepth(tree, top_unigrams[i]))
			depth = max(poss_depths)
			if depth == 0: depth = 1
			bit_vector.append(1) #1/float(depth))
		else:
			bit_vector.append(0)

	for i in range(0, len(top_bigrams)):
		if top_bigrams[i] in example: 
			poss_depths = []
			for tree in trees:
				poss_depths.append(findDepth(tree, top_bigrams[i]))
			depth = max(poss_depths)
			if depth == 0: depth = 1
			bit_vector.append(1) # 1/float(depth))
		else:
			bit_vector.append(0)

	for i in range(0, len(top_trigrams)):
		if top_trigrams[i] in example: 
			poss_depths = []
			for tree in trees:
				poss_depths.append(findDepth(tree, top_trigrams[i]))
			depth = max(poss_depths)
			if depth == 0: depth = 1
			bit_vector.append(1) # 1/float(depth))
		else:
			bit_vector.append(0)

	# modifierPercentage feature

	bit_vector.append(modifierPercentage(example, prs))

	# header length feature
 
	bit_vector.append(len(example.split()))

	# max parse tree depth

	tree_depths = []
	for tree in trees: 
		tree_depths.append(get_depth(tree))

	bit_vector.append(max(tree_depths))	

	return bit_vector

def insert_into_db():
	db = MySQLdb.connect('localhost', 'root', 'glassesandhair', "stocks")
	c = db.cursor()

	infile = open("GOOG_NEWS.csv", "r")

	dates = []
	headlines = []

	running_headline = ""
	running_date = ""
	corpus = ""

	for line in infile:
		arr = line.split('","')
		arr[0] = arr[0][1:]
		arr[4] = arr[4][:-2]
		headline = arr[0]
		date = arr[4]
		if (date != running_date):
			if running_headline != '':
				dates.append(official_date)
				headlines.append(running_headline)
			running_date = date
			running_headline = headline
			official_date = time.strptime(date, "%d-%b-%y")
		else:
			running_headline += ". " + headline
		corpus += " " + headline

	tokens = corpus.split()
	unigram_counts = {}
	for t in tokens:
		if t in unigram_counts:
			unigram_counts[t] += 1
		else:
			unigram_counts[t] = 1

	bigram_counts = {}
	for i in range(0, len(tokens) - 1):
		b = tokens[i - 1] + " " + tokens[i]
		if b in bigram_counts:
			bigram_counts[b] += 1
		else:
			bigram_counts[b] = 1

	trigram_counts = {}
	for i in range(0, len(tokens) - 2):
		t = tokens[i - 2] + " " + tokens[i - 1] + " " + tokens[i]
		if t in trigram_counts:
			trigram_counts[t] += 1
		else:
			trigram_counts[t] = 1

	top_unigrams = sorted(unigram_counts, key = unigram_counts.get, reverse = True)[:30]
	top_bigrams = sorted(bigram_counts, key = bigram_counts.get, reverse = True)[:30]
	top_trigrams = sorted(trigram_counts, key = trigram_counts.get, reverse = True)[:30]

	print top_unigrams
	print top_bigrams
	print top_trigrams

	f = open('touch update_queries_goog_nodepth', 'w')

	for i in range(0, len(dates)):
		date = dates[i]
		headline = headlines[i]
		m_d = time.strftime('%Y-%m-%d %H:%M:%S', date)

		query = "SELECT * FROM goog_info_depthless where date = '" + m_d + "'"
		c.execute(query)
		results = c.fetchall()

		if len(results) > 0: 
			bv = bitVector(headline, top_unigrams, top_bigrams, top_trigrams)
			print date
			uq = "UPDATE goog_info_depthless SET "
			uq += "uni1 = " + str(bv[0]) + ", "
			uq += "uni2 = " + str(bv[1]) + ", "
			uq += "uni3 = " + str(bv[2]) + ", "
			uq += "uni4 = " + str(bv[3]) + ", "
			uq += "uni5 = " + str(bv[4]) + ", "
			uq += "uni6 = " + str(bv[5]) + ", "
			uq += "uni7 = " + str(bv[6]) + ", "
			uq += "uni8 = " + str(bv[7]) + ", "	
			uq += "uni9 = " + str(bv[8]) + ", "
			uq += "uni10 = " + str(bv[9]) + ", "
			uq += "uni11 = " + str(bv[10]) + ", "
			uq += "uni12 = " + str(bv[11]) + ", "
			uq += "uni13 = " + str(bv[12]) + ", "
			uq += "uni14 = " + str(bv[13]) + ", "
			uq += "uni15 = " + str(bv[14]) + ", "
			uq += "uni16 = " + str(bv[15]) + ", "
			uq += "uni17 = " + str(bv[16]) + ", "
			uq += "uni18 = " + str(bv[17]) + ", "	
			uq += "uni19 = " + str(bv[18]) + ", "
			uq += "uni20 = " + str(bv[19]) + ", "
			uq += "uni21 = " + str(bv[20]) + ", "
			uq += "uni22 = " + str(bv[21]) + ", "
			uq += "uni23 = " + str(bv[22]) + ", "
			uq += "uni24 = " + str(bv[23]) + ", "
			uq += "uni25 = " + str(bv[24]) + ", "
			uq += "uni26 = " + str(bv[25]) + ", "
			uq += "uni27 = " + str(bv[26]) + ", "
			uq += "uni28 = " + str(bv[27]) + ", "	
			uq += "uni29 = " + str(bv[28]) + ", "
			uq += "uni30 = " + str(bv[29]) + ", "
			uq += "bi1 = " + str(bv[30]) + ", "
			uq += "bi2 = " + str(bv[31]) + ", "
			uq += "bi3 = " + str(bv[32]) + ", "
			uq += "bi4 = " + str(bv[33]) + ", "
			uq += "bi5 = " + str(bv[34]) + ", "
			uq += "bi6 = " + str(bv[35]) + ", "
			uq += "bi7 = " + str(bv[36]) + ", "
			uq += "bi8 = " + str(bv[37]) + ", "	
			uq += "bi9 = " + str(bv[38]) + ", "
			uq += "bi10 = " + str(bv[39]) + ", "
			uq += "bi11 = " + str(bv[40]) + ", "
			uq += "bi12 = " + str(bv[41]) + ", "
			uq += "bi13 = " + str(bv[42]) + ", "
			uq += "bi14 = " + str(bv[43]) + ", "
			uq += "bi15 = " + str(bv[44]) + ", "
			uq += "bi16 = " + str(bv[45]) + ", "
			uq += "bi17 = " + str(bv[46]) + ", "
			uq += "bi18 = " + str(bv[47]) + ", "	
			uq += "bi19 = " + str(bv[48]) + ", "
			uq += "bi20 = " + str(bv[49]) + ", "
			uq += "bi21 = " + str(bv[50]) + ", "
			uq += "bi22 = " + str(bv[51]) + ", "
			uq += "bi23 = " + str(bv[52]) + ", "
			uq += "bi24 = " + str(bv[53]) + ", "
			uq += "bi25 = " + str(bv[54]) + ", "
			uq += "bi26 = " + str(bv[55]) + ", "
			uq += "bi27 = " + str(bv[56]) + ", "
			uq += "bi28 = " + str(bv[57]) + ", "	
			uq += "bi29 = " + str(bv[58]) + ", "
			uq += "bi30 = " + str(bv[59]) + ", "
			uq += "tri1 = " + str(bv[60]) + ", "
			uq += "tri2 = " + str(bv[61]) + ", "
			uq += "tri3 = " + str(bv[62]) + ", "
			uq += "tri4 = " + str(bv[63]) + ", "
			uq += "tri5 = " + str(bv[64]) + ", "
			uq += "tri6 = " + str(bv[65]) + ", "
			uq += "tri7 = " + str(bv[66]) + ", "
			uq += "tri8 = " + str(bv[67]) + ", "	
			uq += "tri9 = " + str(bv[68]) + ", "
			uq += "tri10 = " + str(bv[69]) + ", "
			uq += "tri11 = " + str(bv[70]) + ", "
			uq += "tri12 = " + str(bv[71]) + ", "
			uq += "tri13 = " + str(bv[72]) + ", "
			uq += "tri14 = " + str(bv[73]) + ", "
			uq += "tri15 = " + str(bv[74]) + ", "
			uq += "tri16 = " + str(bv[75]) + ", "
			uq += "tri17 = " + str(bv[76]) + ", "
			uq += "tri18 = " + str(bv[77]) + ", "	
			uq += "tri19 = " + str(bv[78]) + ", "
			uq += "tri20 = " + str(bv[79]) + ", "
			uq += "tri21 = " + str(bv[80]) + ", "
			uq += "tri22 = " + str(bv[81]) + ", "
			uq += "tri23 = " + str(bv[82]) + ", "
			uq += "tri24 = " + str(bv[83]) + ", "
			uq += "tri25 = " + str(bv[84]) + ", "
			uq += "tri26 = " + str(bv[85]) + ", "
			uq += "tri27 = " + str(bv[86]) + ", "
			uq += "tri28 = " + str(bv[87]) + ", "	
			uq += "tri29 = " + str(bv[88]) + ", "
			uq += "tri30 = " + str(bv[89]) + ", "
			uq += "feat1 = " + str(bv[90]) + ", "
			uq += "feat2 = " + str(bv[91]) + ", "
			uq += "feat3 = " + str(bv[92])
			uq += " where date = '" + m_d + "'"
			f.write(uq + '\n')
