import re
import csv
from itertools import zip_longest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import string
import math
start_t = time.time()


def line_1(i):
    l = []
    for x in i:
        if (x).isalnum():
            if x == "â":
                l.append("'")
            elif x in string.ascii_letters:
                l.append(x)
    return("".join(l))


def func_edit(l_word):
    l_new = []
    for i in l_word.split(" "):
        i = re.sub(r"\n", "", i)
        l_new.append(i)
        for x in list(i):
            if not (x).isalnum() and x != ".":
                l_new[l_new.index(i)] = line_1(i)
                break
    return(" ".join(l_new))


# extract words
word = open(
    r"words\words1.txt", "r")
words = word.read()

words_regular = re.sub(r",", "", words)

word_list = words_regular.split(" ")
words_list = []
for word in word_list:
    if(len(word.split())) > 1:
        for w in (word.split()):
            try:
                (int(w)/2)
            except:
                words_list.append(w)
    else:
        words_list.append(word)

for word in words_list:
    if '\n' in word:
        words_list[words_list.index(word)] = (re.sub("\n", "", word))
# extract pharses
myFile = open(
    r"rest of the book\book1.txt", "r")

word_book = myFile.readlines()

wordBook_list = []
explain_list = []
example_list = []
l_number = 0
for word in words_list:
    for line in word_book[:]:
        if f" {word} " in line.lower() and (" adj." in line or " n." in line or " v." in line or " prep." in line or "[" in line or "]" in line):
            wordBook_list.append(word)

            explain_list.append(func_edit(word_book[word_book.index(line)+1]))

            example_list.append(func_edit(word_book[word_book.index(line)+2]))
            l_number = word_book.index(line)+3
            break
        elif "[" in line and (word == (re.sub(" ", "", line[:line.index("[")].lower())) or word == (re.sub(" ", "", line[1:line.index("[")].lower()))):
            wordBook_list.append(word)

            explain_list.append(func_edit(word_book[word_book.index(line)+1]))

            example_list.append(func_edit(word_book[word_book.index(line)+2]))
            break
part = 0

print(len(wordBook_list))
print(len(example_list))
print(len(explain_list))

# ---------------------------------


def word_arabic(cl, o, y):
    whole_words = ""
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(
        "https://www.google.com/search?q=translate&oq=tr&aqs=chrome.0.69i59l2j69i57j69i60l5.938j0j7&sourceid=chrome&ie=UTF-8")

    x = 0
    for i in range((math.ceil((len(cl)/o)))):
        e = ("\n".join(cl[int(x):int(y)]))

        browser.find_element_by_tag_name("textarea").send_keys(e)
        time.sleep(2)
        translate_w = browser.find_elements_by_tag_name(
            "pre span")
        t = translate_w[2].get_attribute("innerHTML")
        whole_words += t+"\n"
        browser.find_element_by_tag_name("textarea").clear()

        x = y
        y += o

    time.sleep(5)
    browser.quit()
    return whole_words


wordBook_list_arabic = []
wordBook_list_a = word_arabic(wordBook_list, 100.0, 100)
for w in wordBook_list_a.splitlines():
    wordBook_list_arabic.append(re.sub(r"\n", "", w))


def explain_list_func():
    explain_list_a = word_arabic(explain_list, 20.0, 20)
    explain_list_arabic = []
    for w in explain_list_a.splitlines():
        explain_list_arabic.append(re.sub(r"\n", "", w))
    return explain_list_arabic


explain_list_arabic = explain_list_func()


def example_list_func():
    example_list_a = word_arabic(example_list, 20.0, 20)
    example_list_arabic = []
    for w in example_list_a.splitlines():
        example_list_arabic.append(re.sub(r"\n", "", w))
    return example_list_arabic


example_list_arabic = example_list_func()


file_lest = [wordBook_list, wordBook_list_arabic, explain_list,
             explain_list_arabic, example_list, example_list_arabic]
exported = zip_longest(*file_lest)
with open(r"course_english_1.csv", "w", encoding="utf-8-sig'") as myfile:
    wr = csv.writer(myfile)
    wr.writerows(exported)

print(f"TIME IS = {(time.time()-start_t)/60} minute")
