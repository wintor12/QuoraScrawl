
# coding: utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os, re, sys

def readHtml(path):
    p = open(path, 'r')
    st = p.read()
    p.close()
    return st

def removeHttpFromText(path):
    ans_names = os.listdir(path)
    for name in ans_names:
        p = open(path + name, 'r')
        s = p.read()
        p.close()
        s = re.sub(r"http\S+", "", s)
        with open(path + name, 'w') as p:
            p.write(s)

def getTextAndName(path, maxsize = sys.maxint, minsize = -1, unique = True):
    answers = []
    ans_names = os.listdir(path)
    ans_names.sort(key=lambda x: int(x.split('_')[0]))
    names = []
    for name in ans_names:
        if os.path.getsize(path + name) <= maxsize and os.path.getsize(path + name) >= minsize:
            p = open(path + name, 'r')
            s = p.read()
            p.close()
            if unique:
                if s not in answers:
                    names.append(name)
                    answers.append(s)
            else:
                names.append(name)
                answers.append(s) 
    return answers, names

def getNames(path):
    ans_names = os.listdir(path)
    ans_names.sort(key=lambda x: int(x.split('_')[0]))
    return ans_names

def copyFiles2Folder(names, spath, dpath):
    for name in names:
        shutil.copyfile(spath + name, dpath + name)
        
def st2num(st):
    if st.endswith('k'):
        return int(float(st[:-1])*1000)
    elif st.endswith('m'):
        return int(float(st[:-1])*1000000)
    else:
        return int(st)

def getAnswerCount(soup):
    ansdiv = soup.find("div", { "class" : "AnswerPagedList PagedList" })
    soup = BeautifulSoup(str(ansdiv))
    ans = soup.findAll("div", { "class" : "pagedlist_item" })
    n = 0
    for answer in ans:
        soup = BeautifulSoup(str(answer))
        if soup.find("div", { "class" : "CollapsedAnswersSectionCollapsed SimpleToggle Toggle" }) is not None:
            n = n + 1
    return len(ans) - n

def getUpvotes(soup):
    s = soup.find("a", { "class" : 
            "Answer Upvote Button TwoStateButton primary_action answer_upvote main_button" })
    if s is None:
        print "upvote none found! \n" + getText(soup) 
        return 0
    else:
        return st2num(s.text[6:])

def getViews(soup):
    s = soup.find("span", { "class" : "meta_num" })
    if s is None:
        print 'view none found!\n' + getText(soup)
        return 0
    else:
        return st2num(s.text)

def getCommentCount(soup):
    s = soup.find("a", { "class" : "view_comments comment_link" })
    s = BeautifulSoup(str(s))
    s = s.find("span", { "class" : "count" })
    if s is None:
        print 'count none found!\n'
        return 0
    else:
        return s.text

def getText(soup):
    s = soup.find("div", { "class" : "Answer AnswerPageAnswer AnswerBase" })
    if s is None:
        s = soup.find("div", { "class" : 
            "AnswerExpandable SimpleToggle Toggle Expandable AnswerEditableExpandable" })
    soup = BeautifulSoup(str(s))
    ##Sometimes question also in rendered_qtext
    s = soup.findAll("span", { "class" : "rendered_qtext" })
    if len(s) == 0:
        return 'Answer deleted'
    elif len(s) == 1:
        return s[0].text
    else:
        return s[1].text
    

### No text has been cleaned up yet. Remember to call it after read text from txt file
def cleanText(text):
    text = re.sub("\n+","\n",text)
    text = re.sub(r"http\S+", "", text)
        

def getUserName(soup):
    s = soup.find("a", { "class" : "user" })
    if s is None:
        return 'Anonymous'
    else:
        return s.text

def getAnswerUrl(soup):
    s = soup.find("a", { "class" : "answer_permalink" })
    if s is None: ##can not get user link because the text is not full expanded, 'more'
        return 'more'
    return 'https://www.quora.com/'+s['href']

def getTime(soup):
    s = soup.find("a", { "class" : "answer_permalink" })
    if s is None:
        return 'Null'
    return s.text

def getUserFollow(soup):
    s = soup.find("a", { "class" : "Button TwoStateButton User main_button user_follow_button" })
    soup = BeautifulSoup(str(s))
    s = soup.find("span", { "class" : "count" })
    if s is None:
        return 'Null'
    return st2num(s.text)

def getNumPic(soup):
    s = soup.find("div", { "class" : "Answer AnswerPageAnswer AnswerBase" })
    if s is None:
        s = soup.find("div", { "class" : 
            "AnswerExpandable SimpleToggle Toggle Expandable AnswerEditableExpandable" })
    soup = BeautifulSoup(str(s))
    ##Sometimes question also in rendered_qtext
    s = soup.findAll("div", { "class" : "qtext_image_wrapper" })
    s2 = soup.findAll("div", { "class" : "qtext_embed thumbnail" })
    return len(s) + len(s2)

def getTextWithNewline(soup):
    s = soup.find("div", { "class" : "Answer AnswerPageAnswer AnswerBase" })
    if s is None:
        s = soup.find("div", { "class" : 
            "AnswerExpandable SimpleToggle Toggle Expandable AnswerEditableExpandable" })
    soup = BeautifulSoup(str(s))
    ##Sometimes question also in rendered_qtext
    s = soup.findAll("span", { "class" : "rendered_qtext" })
    if len(s) == 0:
        return 'Answer deleted'
    elif len(s) == 1:
        soup = BeautifulSoup(str(s[0]))
        ## split paragraph with \n
        result = soup.findAll("p", { "class" : "qtext_para" })
        if len(result) > 0:
            result = [r.text for r in result]
            return '\n'.join(result)
        else:
            single_para = re.sub("(</?\s*br\s*/?>\s*)+", "\n", str(s[0]))
            ##replace <h2> with \n
            single_para = re.sub("</?\s*h[1-9]\s*/?>", "\n", single_para)
            return BeautifulSoup(single_para).text
    else:
        soup = BeautifulSoup(str(s[1]))
        result = soup.findAll("p", { "class" : "qtext_para" })
        if len(result) > 0:
            result = [r.text for r in result]
            return '\n'.join(result)
        else:
            single_para = re.sub("(</?\s*br\s*/?>\s*)+", "\n", str(s[1]))
            single_para = re.sub("</?\s*h[1-9]\s*/?>", "\n", single_para)
            return BeautifulSoup(single_para).text
        
def getTextWithNewlineNoedit(soup):
    s = soup.find("div", { "class" : "Answer AnswerPageAnswer AnswerBase" })
    if s is None:
        s = soup.find("div", { "class" : 
            "AnswerExpandable SimpleToggle Toggle Expandable AnswerEditableExpandable" })
    soup = BeautifulSoup(str(s))
    ##Sometimes question also in rendered_qtext
    s = soup.findAll("span", { "class" : "rendered_qtext" })
    if len(s) == 0:
        return 'Answer deleted'
    elif len(s) == 1:
        soup = BeautifulSoup(str(s[0]))
        ## split paragraph with \n
        result = soup.findAll("p", { "class" : "qtext_para" })
        if len(result) > 0:
            newResults = []
            for r in result:
                content = r.text
                if(content.startswith('Edit')):
                    break
                newResults.append(content)
#             result = [r.text for r in result]
            return '\n'.join(newResults)
        else:
            single_para = re.sub("(</?\s*br\s*/?>\s*)+", "\n", str(s[0]))
            ##replace <h2> with \n
            single_para = re.sub("</?\s*h[1-9]\s*/?>", "\n", single_para)
            return BeautifulSoup(single_para).text
    else:
        soup = BeautifulSoup(str(s[1]))
        result = soup.findAll("p", { "class" : "qtext_para" })
        if len(result) > 0:
            newResults = []
            for r in result:
                content = r.text
                if(content.startswith('Edit')):
                    break
                newResults.append(content)
#             result = [r.text for r in result]
            return '\n'.join(newResults)
        else:
            single_para = re.sub("(</?\s*br\s*/?>\s*)+", "\n", str(s[1]))
            single_para = re.sub("</?\s*h[1-9]\s*/?>", "\n", single_para)
            
def saveAnswers(answer_urls, html_path, plain_text_path, startindex):
    browser = webdriver.Chrome()
    browser.get("https://www.quora.com/")
    print "start logging in"
    time.sleep(30)
    print "time is up"
    upvotes = []
    views = []
    comments = []
    times = []
    follows = []
    pics = []
    s = ''
    with open(answer_urls,'r') as p:
        s = p.read()
    lines = s.split('\n')
    for line in lines:
        items = line.split('\t')
        url = items[3]
        index = items[0]
        if int(index) < startindex:
            continue
        question = items[1]
        browser.get(url)
        time.sleep(.8)
        src = browser.page_source
        p = open(html_path + str(index) + '_' + question + '.html', 'w')
        p.write(src.encode('utf-8'))
        p.close()
        soup = BeautifulSoup(src)
    #     text = getText(soup)
        text = getTextWithNewline(soup)
        p = open(plain_text_path + str(index) + '_' + question + '.txt', 'w')
        p.write(text.encode('utf-8'))
        p.close()
        upvotes.append(getUpvotes(soup))
        views.append(getViews(soup))
        comments.append(getCommentCount(soup))
        times.append(getTime(soup))
        follows.append(getUserFollow(soup))
        pics.append(getNumPic(soup))
        print index
    with open(answer_urls[:-4] + '_upvotes.txt','w') as p:
        p.write('\n'.join([str(x) for x in upvotes]))
    with open(answer_urls[:-4] + '_views.txt','w') as p:
        p.write('\n'.join([str(x) for x in views]))
    with open(answer_urls[:-4] + '_comments.txt','w') as p:
        p.write('\n'.join([str(x) for x in comments]))
    with open(answer_urls[:-4] + '_times.txt','w') as p:
        p.write('\n'.join([str(x) for x in times]))
    with open(answer_urls[:-4] + '_follows.txt','w') as p:
        p.write('\n'.join([str(x) for x in follows]))
    with open(answer_urls[:-4] + '_pics.txt','w') as p:
        p.write('\n'.join([str(x) for x in pics]))
    return upvotes, views, comments, times, follows, pics


def saveAttributes(html_path):
    upvotes = []
    views = []
    comments = []
    times = []
    follows = []
    pics = []
    ans_htmls = os.listdir(html_path)
    ans_htmls.sort(key=lambda x: int(x.split('_')[0]))
    for name in ans_htmls:
        index = name.split('_')[0]
        src = readHtml(html_path + name)
        soup = BeautifulSoup(src)
        upvotes.append(getUpvotes(soup))
        views.append(getViews(soup))
        comments.append(getCommentCount(soup))
        times.append(getTime(soup))
        follows.append(getUserFollow(soup))
        pics.append(getNumPic(soup))
        print index
    with open('story_upvotes.txt','w') as p:
        p.write('\n'.join([str(x) for x in upvotes]))
    with open('story_views.txt','w') as p:
        p.write('\n'.join([str(x) for x in views]))
    with open('story_comments.txt','w') as p:
        p.write('\n'.join([str(x) for x in comments]))
    with open('story_times.txt','w') as p:
        p.write('\n'.join([str(x) for x in times]))
    with open('story_follows.txt','w') as p:
        p.write('\n'.join([str(x) for x in follows]))
    with open('story_pics.txt','w') as p:
        p.write('\n'.join([str(x) for x in pics]))
    return upvotes, views, comments, times, follows, pics

