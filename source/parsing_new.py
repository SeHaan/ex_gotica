#%% importing and basic parsing
import xml.etree.ElementTree as et
import pickle as pkl

f = open('gotica_new.xml', 'rt', encoding='utf-8')

gothicTree = et.parse(f)
gothicRoot = gothicTree.getroot()
body = gothicRoot[1][1]

bookList = []
for child in body:
    if child.tag == 'div': bookList.append(child)

chapterList = []
for book in bookList:
    for chapter in book:
        if chapter.tag == 'div' or chapter.tag == 'opener' or chapter.tag == 'closer': chapterList.append(chapter)

abList = []
for chapter in chapterList:
    if chapter.tag == 'opener' or chapter.tag == 'closer':
        abList.append(chapter)
    for ab in chapter:
        if ab.tag == 'ab': abList.append(ab)

rdgList = []
for ab in abList:
    for rdg in ab[0]:
        if rdg.tag == 'rdg': rdgList.append(rdg)

rawList = []
for rdg in rdgList:
    line = ''
    idLine = ''
    for seg in rdg.iter():
        if seg.tag == 'seg' and 'id' in seg.attrib:
            line += seg.text
            line += " "
            idLine += seg.attrib['id']
            idLine += " "
        elif seg.tag == 'c':
            line += seg.text
            line += " "
            idLine += seg.text
            idLine += " "

    line = line.replace('\n         ', '')
    
    rdgDict = dict(id=rdg.attrib['id'], wit=rdg.attrib['wit'], org_line=line, id_line=idLine)
    rawList.append(rdgDict)

with open('raw_gotica.pickle', 'wb') as f:
    pkl.dump(rawList, f)