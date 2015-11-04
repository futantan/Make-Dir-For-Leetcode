#!/usr/bin/env python
# coding=utf-8
import requests
import bs4
import os
import threading

markdownFormat = u"""\
# %(title)s

## Problem：

%(content)s

## Source:
[Leetcode](%(url)s)
"""

algorithmsListUrl = "https://leetcode.com/problemset/algorithms/"
baseUrl = "https://leetcode.com"
baseDir = "./"


def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)

    if not isExists:
        print "making dir " + path + "..."
        os.makedirs(path)
    else:
        print '! ' + path + " already exist"


def writeContentToFile(content, pathToFile):
    with open(pathToFile, 'w') as outputFile:
        outputFile.write(content.encode('utf-8'))


def getMarkDownOfQuestionContentFromUlr(questionUrl):
    response = requests.get(questionUrl)
    soup = bs4.BeautifulSoup(response.text)
    content = soup.find("div", class_="col-md-12")
    # the title of this question
    questionTitle = content.find("div", class_="question-title").h3.string
    # the difficulty of this question
    questionDifficulty = "Difficulty: " + content.find("div", class_="row col-md-12").find_all("span")[2].strong.string

    questionContentTag = content.find_all("div", class_="row")[1].div.div.find_all("p", recursive=False)
    questionContent = soup.new_tag('div')

    for index in range(len(questionContentTag)):
        questionContent.insert(index, questionContentTag[index])

    # the content of this question
    questionContent = questionContent.prettify()

    markdown = markdownFormat % {
        'title': questionTitle,
        'content': questionContent,
        'url': questionUrl
    }

    return markdown


def makeThreadToMakeDir(baseUrl):
    response = requests.get(baseUrl)
    soup = bs4.BeautifulSoup(response.text)
    problemList = soup.find(id="problemListRow").table.tbody
    trs = problemList.find_all("tr")
    # totalCount = len(trs)
    for tr in trs:
        LeetcodeThread(tr).start()


class LeetcodeThread(threading.Thread):
    def __init__(self, tr):
        super(LeetcodeThread, self).__init__()
        self.tr = tr

    def run(self):
        self.makeDirWithProblemTrTag()

    def makeDirWithProblemTrTag(self):
        tds = self.tr.find_all("td")
        sequenceNum = tds[1].string
        a = tds[2].a
        problemName = a.string
        problemUrl = baseUrl + a['href']
        dirName = sequenceNum.rjust(3, '0') + '_' + problemName.replace(' ', '_')
        dirPath = baseDir + dirName
        mkdir(dirPath)
        mdContent = getMarkDownOfQuestionContentFromUlr(problemUrl)
        writeContentToFile(mdContent, dirPath + "/" + "README.MD")


if __name__ == "__main__":
    makeThreadToMakeDir(algorithmsListUrl)