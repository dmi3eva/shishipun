import pymorphy2
morph = pymorphy2.MorphAnalyzer()
word = u'люди'
word  = word.decode('utf-8')
print(morph.parse("люди"))
