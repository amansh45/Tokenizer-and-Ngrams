
import re

INSERT_DELIMETER = ' #*?$^& '
MATCH_DELIMETER = '#*?$^&'
wordToIndex = {"<$>":1, "</$>":2}
indexToWord = {1:"<$>", 2:"</$>"}
wordIndex=3
CHUNKSIZE = 104857600
total_tokens = 0

def createMapping(data):
    global wordIndex
    if data not in wordToIndex.keys():
        wordToIndex[data] = wordIndex
        #indexToWord[wordIndex] = data
        wordIndex+=1

def generate_ngrams(tokens, n):
    i, tsize, ngrams = 0, len(tokens), []
    while i<tsize:
        currSent = []
        while i<tsize and tokens[i] != "2":
            currSent.append(tokens[i])
            i+=1
        currSent.append("2")
        currSize = len(currSent)
        j=0
        while j<=currSize-n:
            ngrams.append(' '.join(currSent[j:j+n]))
            j+=1
        i+=1
    return ngrams

def buildData(bytes_read, punchFlag):
    t_data = []
    opened = False
    selfData = ""
    t_data.append("<$>")
    for x in bytes_read.split(' '):
        if x == MATCH_DELIMETER and not opened:
            opened = True
            continue
        elif x != MATCH_DELIMETER and opened:
            selfData = selfData + x
        elif x == MATCH_DELIMETER:
            t_data.append(selfData.lower())
            createMapping(selfData.lower())
            selfData = ""
            opened = False
        elif x!="":
            # Extracting currency....
            curr = re.search(r"^(\d{1,3})(,\d{1,3})*(\.\d{1,})?$", x)
            if curr:
                createMapping(curr[0])
                t_data.append(curr[0])
            else:
                if punchFlag:
                    # Extracting punctuations....
                    for t in re.findall(r"""[A-Za-z0-9]+|[\W_]+""", x):
                        if t!="":
                            createMapping(t)
                            t_data.append(t)
                else:
                    st = ""
                    for k in x:
                        ch = k.lower()
                        if ch>='a' and ch<='z':
                            st += ch
                    if st!="":
                        createMapping(st)
                        t_data.append(st)
                    
    t_data.append("</$>")
    return t_data

def markNames(bytes_read):
    title = r"^[A-Z][a-z]{1,2}\.$"
    name_regex = r"^[A-Z][a-z][a-z]+$|^[A-Z]\.$"
    modified_data = []
    nameStarted = False
    for x in bytes_read.split(' '):
        a = re.search(title, x)
        b = re.search(name_regex, x)
        if a!=None:
            if not nameStarted:
                modified_data.append(INSERT_DELIMETER)
                nameStarted = True
            modified_data.append(x)
        elif b!=None:
            if nameStarted:
                modified_data.append(x)
            else:
                modified_data.append(INSERT_DELIMETER)
                modified_data.append(x)
                nameStarted = True
        elif nameStarted:
            nameStarted = False
            modified_data.append(INSERT_DELIMETER)
            modified_data.append(x)
        else:
            modified_data.append(x)
    return ' '.join(modified_data)

def processData(bytes_read, punchFlag):
    # Extracting names
    bytes_read = markNames(bytes_read)
    
    # Extracting mails
    mails = re.findall(r'\S+@\S+', bytes_read)
    for i in mails:
        newMail = INSERT_DELIMETER+i+INSERT_DELIMETER
        bytes_read = bytes_read.replace(i, newMail)
    
    # Extracting hashtags
    hashtags = re.findall(r"#(\w+)", bytes_read)
    for i in hashtags:
        newHashTag = INSERT_DELIMETER+"#"+i+INSERT_DELIMETER
        bytes_read = bytes_read.replace("#"+i, newHashTag)
    
    # Extracting mentions
    mention = re.findall(r"@(\w+)", bytes_read)
    for i in mention:
        newMention = INSERT_DELIMETER+"@"+i+INSERT_DELIMETER
        bytes_read = bytes_read.replace("@"+i, newMention)
    
    # Extracting url
    urlRegex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    urls = re.findall(urlRegex, bytes_read)
    for i in urls:
        newUrl = INSERT_DELIMETER+i+INSERT_DELIMETER
        bytes_read = bytes_read.replace(i, newUrl)
        
    # Extracting phone numbers
    numberRegex = r"\d{2,4}-\d{6,7}|\d{3} \d{8}|d{4} \d{8}|\(\d{2,4}\)\d{6,7}|\(\d{2,4}\) \d{6,7}|\+\d{2}-\d{10}|\+\d{2} \d{5} \d{5}|\+\d{2}-\d{5}-\d{5}|\d{5} \d{3} \d{3}|\+\d{2} \d{10}|\d{5}-\d{3}-\d{3}"
    numbers = re.findall(numberRegex, bytes_read)
    for i in numbers:
        newNum = INSERT_DELIMETER+i+INSERT_DELIMETER
        bytes_read = bytes_read.replace(i, newNum)
    
    return buildData(bytes_read, punchFlag)
        
def tokenize(data, tokenize_puntuations=True):
    counter = 0
    t_data = []
    for line in data.split('\n'):
        line = line.replace("'", "")
        t_data += processData(line, tokenize_puntuations)
        counter+=1
        if counter%100000 == 0:
            print("Successfully tokenized ", counter, " rows")
    return t_data

def readFile(file_name, flag=True):
    global indexToWord, wordToIndex, total_tokens
    for curr_file in file_name:
        file = open(curr_file, "r")
        bytes_read = file.readlines(CHUNKSIZE)
        bytes_read = ' '.join(bytes_read)
        k=0
        while bytes_read:
            tokenized_chunk = tokenize(bytes_read, flag)
            k+=1
            print('--------------->',k)
            n_tokens = len(tokenized_chunk)
            total_tokens += n_tokens
            st = '\n'.join(tokenized_chunk)
            t_file = open('data_structures/'+curr_file.split('.')[0]+'_tokens.txt', 'a+')
            t_file.write(st)
            t_file.close()
            bytes_read = file.readlines(CHUNKSIZE)
            bytes_read = ' '.join(bytes_read)
            if k == 2:
                return indexToWord, wordToIndex, total_tokens
    return indexToWord, wordToIndex, total_tokens
