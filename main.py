import os
import sys
import hashlib

split_questions_to_exams = False

lines = []
exams = []
questions = []

hashes = []
dup_questions = []

with open("C:\\test.txt") as f:
    for line in f:
        lines.append(line)

for i in range(len(lines)):
    if lines[i].startswith("Exam ") and questions != []:
        exams.append(questions)
        questions = []
    if lines[i].startswith("QUESTION "):
        question = []
        i += 1
        while lines[i] != 'A.\n': #build question
            question.append(lines[i])
            i += 1
        question = '\n'.join(question)
        
        
        
        #hash stuff to avoid duplicate questions
        the_hash = hashlib.sha1(question).digest()
        if the_hash in hashes:
            dup_questions.append(question)
            continue
        hashes.append(the_hash)
        
        
        
        question = [question]
        answers = []
        while lines[i].startswith("Answer: ") != True:
            if lines[i][0].strip().isalpha() and lines[i][0].strip().isupper() and len(lines[i].strip()) == 2:
                answers.append(lines[i+1])
            i += 1
        question.append(answers)
        question.append(lines[i][8:].strip()) #add a correct answer to the list
        
        
        #what this does:
        #maps A-X answers to array indices and appends a list of correct answers to the question
        question.append([question[1][ord(x)-ord('A')] for x in question[-1]]) #add a full correct answer to the list
        
        
        i += 1
        while lines[i].startswith("Explanation/Reference:") != True:
            i += 1
        
        i += 1
        '''
        ref = []
        while i+1 < len(lines) and lines[i+1].startswith("QUESTION ") != True: #get reference text
            ref.append(lines[i+1].strip())
            i += 1
        ref = '\n'.join(ref)
        if ref == '\n': #get rid of unnecessary newline if the ref is empty
            ref = ""
        '''
        ref = ''
        while i < len(lines) and lines[i].startswith("Exam") != True and lines[i].startswith("QUESTION") != True:
            ref += lines[i]
            i += 1
        ref = ref.strip()
        if ref == '\n':
            ref = ''
        question.append(ref.replace("\n", "<br />"))
        
        questions.append(question)
exams.append(questions)
'''
with open("C:\\output.csv", 'w') as f:
    for e in exams:
        for q in e:
            qu = q[0].replace("\n", "<br />")
            an = q[6].replace("\n", "<br />")
            f.write(qu + "~" + an + "\n")
'''
# question, [A B C etc], answer abcd, full answer, ref
#     0          1           2             3        4
def write_question_to_file(file, q):
    qu = q[0]
    answers = ""
    for ii in range(len(q[1])):
        answers = answers + chr(ii + ord('A')) + '. ' + q[1][ii] + "<br /><br />"
    
    qu = (qu + "<br />Answers:<br /><br />" + answers).replace("\n", "<br />")
    
    #an = (q[2] + ". " + q[3]).replace("\n", "<br />")
    an = ""
    for ii in range(len(q[2])):
        an = an + q[2][ii] + '. ' + q[1][ord(q[2][ii])-ord('A')].strip() + "<br /><br />"
    
    if q[4] != '':
        an += "<br /><br />Explanation/Reference:<br />" + q[4]
    file.write(qu + "~" + an + "\n")

if split_questions_to_exams:
    for x in range(len(exams)):
        with open("C:\\output_" + str(x) + ".csv", 'w') as f:
            for q in exams[x]:
                write_question_to_file(f, q)
                '''
                qu = q[0]
                answers = ""
                for ii in range(len(q[1])):
                    answers = answers + chr(ii + ord('A')) + '. ' + q[1][ii] + "<br /><br />"
                
                qu = (qu + "<br />Answers:<br /><br />" + answers).replace("\n", "<br />")
                
                #an = (q[2] + ". " + q[3]).replace("\n", "<br />")
                an = ""
                for ii in range(len(q[2])):
                    an = an + q[2][ii] + '. ' + q[1][ord(q[2][ii])-ord('A')].strip() + "<br /><br />"
                
                f.write(qu + "~" + an + "\n")
                '''
else:
    with open("C:\\output.csv", 'w') as f:
        for e in exams:
            for q in e:
                write_question_to_file(f, q)


'''
for e in exams:
    for q in e:
        if len(q) < 8:
            print q[0]
            break
'''






















