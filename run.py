#!/usr/bin/env python
# coding=utf-8
import requests
import bs4
import os
import threading
import time
import sys

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
repoReadMeContent = "|Problem|Completed|\n| - | - |\n"


def mkdir(path, withPrint=True):
    path = path.strip()
    isExists = os.path.exists(path)

    if not isExists:
        if withPrint:
            print "making dir " + path + "..."
        os.mkdir(path)
        return True
    else:
        if withPrint:
            print '! ' + path + " already exist"
        return False


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
    # questionDifficulty = "Difficulty: " + content.find("div", class_="row col-md-12").find_all("span")[2].strong.string

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


def getSequenceNumWithProblemNameFromTr(tr, replaceSpaceWithUnderLine=True):
    tds = tr.find_all("td")
    sequenceNum = tds[1].string
    a = tds[2].a  # content
    problemName = a.string
    problemUrl = baseUrl + a['href']
    placeholder = '_' if replaceSpaceWithUnderLine else ' '
    sequenceNumWithProblemName = sequenceNum.rjust(3, '0') + placeholder + problemName.replace(' ', placeholder)
    dirPath = os.path.join(baseDir, sequenceNumWithProblemName)

    isProblemLocked = tds[2].find("i") is not None
    return {'problemUrl': problemUrl,
            'sequenceNumWithProblemName': sequenceNumWithProblemName,
            'dirPath': '' if isProblemLocked else dirPath}


def configBaseDirPath():
    global baseDir
    count = len(sys.argv)
    if count == 1:
        return
    if count > 2:
        print 'please check the directory path'
    else:
        baseDir = sys.argv[1]
        mkdir(baseDir, withPrint=False)


def makeThreadToMakeDir(url):
    if not os.path.isdir(baseDir):
        return

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    problemList = soup.find(id="problemListRow").table.tbody
    trs = reversed(problemList.find_all("tr"))
    # totalCount = len(trs)
    global repoReadMeContent

    for tr in trs:
        result = getSequenceNumWithProblemNameFromTr(tr, False)
        if result['dirPath'] == '':
            continue
        else:
            line = "|[%(sequenceNumWithProblemName)s](%(dirPath)s)| |\n" % {
                'sequenceNumWithProblemName': result['sequenceNumWithProblemName'],
                'dirPath': result['dirPath']
            }
            repoReadMeContent += line

            LeetcodeThread(tr).start()
            time.sleep(0.1)  # if request too fast, will get an error which says "Connection reset by peer"

    writeContentToFile(repoReadMeContent, os.path.join(baseDir, 'README.md'))


class LeetcodeThread(threading.Thread):
    def __init__(self, tr):
        super(LeetcodeThread, self).__init__()
        self.tr = tr

    def run(self):
        self.makeDirWithProblemTrTag()

    def makeDirWithProblemTrTag(self):
        # (problemUrl, sequenceNumWithProblemName, dirPath) = getSequenceNumWithProblemNameFromTr(self.tr)
        result = getSequenceNumWithProblemNameFromTr(self.tr)

        isMkdirSucceed = mkdir(result['dirPath'])
        if not isMkdirSucceed:
            return

        mdContent = getMarkDownOfQuestionContentFromUlr(result['problemUrl'])
        writeContentToFile(mdContent, result['dirPath'] + "/" + "README.md")


if __name__ == "__main__":
    configBaseDirPath()
    makeThreadToMakeDir(algorithmsListUrl)
