#%%
f = open('gotica.xml', 'rt', encoding='utf-8')

lines = f.readlines()

new_text = ''
for line in lines:
    new_text += line.replace('<unclear>', '(unclear)').replace('</unclear>', '(/unclear)').replace('<add>', '(add)').replace('</add>', '(add)')


with open('gotica_new.xml', 'w', encoding='utf-8') as nf:
    nf.write(new_text)
    nf.close()