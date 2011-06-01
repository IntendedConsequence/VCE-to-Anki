import re
import sys
import os
import codecs
import hashlib
import anki

from anki.importing import Importer, ForeignCard
from anki.deck import DeckStorage
from anki.stdmodels import BasicModel

class VceImporter(Importer):
    def __init__(self, *args):
        Importer.__init__(self, *args)
        self.orda = ord('A')
    
    def format_question(self, raw):
        question = {}
        raw = re.split(r'^Explanation\/Reference:', raw, flags=re.S|re.M)
        question['explanation'] = (raw[1].strip())
        raw = re.split(r'^Section:', raw[0], flags=re.S|re.M)
        question['section'] = (raw[1].strip())
        raw = re.split(r'^Answer:', raw[0], flags=re.S|re.M)
        question['answer'] = [ord(c) - self.orda for c in raw[1].strip()]
        raw = re.split(r'^[A-Z]\.$', raw[0], flags=re.M)
        question['answers'] = [a.strip() for a in raw[1:]]
        question['question'] = raw[0].strip()
    
        return question
    
    def foreignCards(self):
        lines = ''
        with open("C:\\test.txt", 'r') as f:
            for line in f:
                lines += line

        exams = [x.strip() for x in re.split(r'^Exam [A-Z]$', lines, flags=re.MULTILINE)[1:]]
        exams = [re.split(r'^QUESTION [0-9][0-9]?[0-9]?', x, flags=re.MULTILINE)[1:] for x in exams]
        exams = [[q.strip() for q in x] for x in exams]

        #orda = ord('A')
        hashes = []
    
        exams = [[self.format_question(q) for q in e] for e in exams]
        n = '\n'
        br = '<br />'
    
        cards = []
        for e in exams:
            for q in e:
                the_hash = hashlib.sha1(q['question']).digest()
                if the_hash in hashes:
                    continue
                hashes.append(the_hash)
    
                front = q['question'] + n*3 + 'Answers:\n\n' + (n*2).join([chr(x + self.orda) + '. ' + q['answers'][x] for x in range(len(q['answers']))])
                back = (n*2).join([chr(a + self.orda) + '. ' + q['answers'][a] for a in q['answer']]) + n*3 + q['explanation']
                
                card = ForeignCard()
                card.fields = [unicode(front.replace(n, br), "utf-8"), unicode(back.replace(n, br), "utf-8")]
                cards.append(card)
        return cards
    
    def fields(seld):
        return 2

deck = DeckStorage.Deck(r'C:\test.anki')
deck.addModel(BasicModel())
imp = VceImporter(deck, '')

imp.doImport()

deck.save()
deck.close()
'''
with open("C:\\output_v2.csv", 'w') as f:
        for e in exams:
            for q in e:
                the_hash = hashlib.sha1(q['question']).digest()
                if the_hash in hashes:
                    continue
                hashes.append(the_hash)
    
                front = q['question'] + n*3 + 'Answers:\n\n' + (n*2).join([chr(x + orda) + '. ' + q['answers'][x] for x in range(len(q['answers']))])
                back = (n*2).join([chr(a + orda) + '. ' + q['answers'][a] for a in q['answer']]) + n*3 + q['explanation']
                
                f.write(front.replace(n, br) + '~' + back.replace(n, br) + n)'''