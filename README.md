Make-Dir-For-Leetcode [中文](#readmechinese)
=====================
## Demo

[Dir-For-Leetcode](https://github.com/futantan/Dir-For-LeetCode)

![](/img/image1.png)

![](/img/image2.png)

## What

This script will create a folder for LeetCode, in each subfolder there will be a file named `README.md`, the content of this file will be the corresponding problem content of LeetCode.

## Who

If you'd like to use LeetCode to practice you algorithms skills and willing to share your code with others on github, this is right for you!

It might not suitable for you if you only want to read it on your own computer because the `README.md` file contains html code which is hard to read, but if you can convert it to markdown and preview it, it will be nice too.

## Setup

That's easy.

```
git clone https://github.com/futantan/Make-Dir-For-Leetcode.git
pip install requests BeautifulSoup4
python run.py pathToDirectoryYouWant
```

Notice that you can add the path you like behind the command, if not, it will be created in current folder.

## Trick

If you do not have the python environment you can just fork the [Dir-For-Leetcode](https://github.com/futantan/Dir-For-LeetCode) repository as you need.

enjoy~

---
<a name="readmechinese"></a>
README(Chinese)
===============

## Make-Dir-For-Leetcode 是什么

该脚本将会在指定的目录建立一个 Leetcode 项目文件夹，每个文件夹中都会有一个 `README.md` 文件，文件的内容是相应文件夹的 Leetcode 题目内容。

## Make-Dir-For-Leetcode 适合哪些人

如果你喜欢使用 Leetcode 来锻炼你的算法，并且愿意使用 github 来开源管理你的算法实现，本项目就适合你。

如果你只是想在本地浏览，请不要使用该脚本，该脚本的 `README.md` 文件中有很多都是可读性很差的 html 代码，但是如果你放在 github 上就会非常漂亮。当然，如果你可以使用本地 Markdown 转换工具，也是可以的。

## Setup

安装非常简单

```
git clone https://github.com/futantan/Make-Dir-For-Leetcode.git
pip install requests BeautifulSoup4
python run.py pathToDirectoryYouWant
```

`python run.py` 后可跟一个表示文件夹路径的参数，如果没有，默认为当前目录。

## 嗯。。。

如果你懒得跑代码的话，直接fork [Dir-For-Leetcode](https://github.com/futantan/Dir-For-LeetCode) 项目也是可以的
