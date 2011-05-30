import re
import sys
import os
import hashlib

lines = ''
with open("C:\\test.txt", 'r') as f:
    for line in f:
        lines += line

exams = [x.strip() for x in re.split(r'^Exam [A-Z]$', lines, flags=re.MULTILINE)[1:]]
exams = [re.split(r'^QUESTION [0-9][0-9]?[0-9]?', x, flags=re.MULTILINE)[1:] for x in exams]
exams = [[q.strip() for q in x] for x in exams]

orda = ord('A')
hashes = []




def format_question(raw):
    question = {}
    raw = re.split(r'^Explanation\/Reference:', raw, flags=re.S|re.M)
    question['explanation'] = (raw[1].strip())
    raw = re.split(r'^Section:', raw[0], flags=re.S|re.M)
    question['section'] = (raw[1].strip())
    raw = re.split(r'^Answer:', raw[0], flags=re.S|re.M)
    question['answer'] = [ord(c) - orda for c in raw[1].strip()]
    raw = re.split(r'^[A-Z]\.$', raw[0], flags=re.M)
    question['answers'] = [a.strip() for a in raw[1:]]
    question['question'] = raw[0].strip()
    
    
    
    return question

exams = [[format_question(q) for q in e] for e in exams]
n = '\n'
br = '<br />'

with open("C:\\output_v2.csv", 'w') as f:
        for e in exams:
            for q in e:
                the_hash = hashlib.sha1(q['question']).digest()
                if the_hash in hashes:
                    continue
                hashes.append(the_hash)
    
                front = q['question'] + n*3 + 'Answers:\n\n' + (n*2).join([chr(x + orda) + '. ' + q['answers'][x] for x in range(len(q['answers']))])
                back = (n*2).join([chr(a + orda) + '. ' + q['answers'][a] for a in q['answer']]) + n*3 + q['explanation']
                
                f.write(front.replace(n, br) + '~' + back.replace(n, br) + n)