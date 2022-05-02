#%% open
import pickle as pkl
import pandas as pd
from tqdm import tqdm

with open('raw_gotica.pickle', 'rb') as f:
    raw_data = pkl.load(f)

f.close()
df_raw = pd.DataFrame(raw_data)
df_split = df_raw.copy()
del raw_data

target_lem = 'magan'

#%% data loading
df_analyses = pd.read_csv('0_Analyses.csv', encoding='utf-8')
df_lemmata = pd.read_csv('0_Lemmata.csv', encoding='utf-8')
df_gomorphTags = pd.read_csv('0_GomorphTags.csv', encoding='utf-8')
df_gomorph = pd.read_csv('0_Gomorph.csv', encoding='utf-8')
df_pos = pd.read_csv('0_POSTags.csv', encoding='utf-8')
df_books = pd.read_csv('0_books.csv', encoding='utf-8')
df_segments = pd.read_csv('0_Segments.csv', encoding='utf-8')
df_manuscripts = pd.read_csv('0_Manuscripts.csv', encoding='utf-8')

# lemmata -> gomorph / POS / analyses
PartOfSpeech = df_lemmata.loc[df_lemmata['Lemma'] == target_lem].iloc[0]['POS']
Morphology = df_lemmata.loc[df_lemmata['Lemma'] == target_lem].iloc[0]['Morphology']
Lemma = df_lemmata.loc[df_lemmata['Lemma'] == target_lem].iloc[0]['ID']

# Analyses -> gomorphTags / token
df_search = df_analyses[df_analyses['Lemma'] == Lemma]
Tokens = []
GomorphTagsIds = []

for tk in enumerate(df_search['Token']):
    Tokens.append(tk[1])

for mt in enumerate(df_search['Tag']):
    GomorphTagsIds.append(mt[1])

# POS and Morpheme
TokenPOS = df_pos[df_pos['ID'] == PartOfSpeech].iloc[0]['Name']
Morpheme = df_gomorph[df_gomorph['ID'] == Morphology].iloc[0]['Name']

# token listing from raw_data
for tknum in range(len(df_split['org_line'])):
    df_split.loc[tknum, 'org_line'] = df_split.loc[tknum, 'org_line'].split(' ')
    df_split.loc[tknum, 'id_line'] = df_split.loc[tknum, 'id_line'].split(' ')

#%% Searching line including target tokens
search_SegId = []
search_line = []
search_morphtag = []

for token in tqdm(Tokens):
    token_s = 'T' + str(token)
    for line in enumerate(df_split['id_line']):
        if token_s in line[1]:
            pos = line[1].index(token_s)
            try:
                new_token = df_split.loc[line[0], 'org_line'][pos]
                new_line = df_raw.loc[line[0], 'org_line'].replace(new_token, '▶' + new_token + '◀')
                search_line.append(new_line)
            except IndexError:
                search_line.append(df_raw.loc[line[0], 'org_line'])
            search_SegId.append(df_raw.loc[line[0], 'id'])

#%% reference tagging
search_ref = []

for segId in search_SegId:
    seg = int(segId[1:])
    num_book = df_segments[df_segments['ID'] == seg].iloc[0]['Book']
    num_man = df_segments[df_segments['ID'] == seg].iloc[0]['Manuscript']
    num_N1 = df_segments[df_segments['ID'] == seg].iloc[0]['N1']
    num_N2 = df_segments[df_segments['ID'] == seg].iloc[0]['N2']

    man = df_manuscripts[df_manuscripts['ID'] == num_man].iloc[0]['Code']
    book = df_books[df_books['ID'] == num_book].iloc[0]['Code']

    ref = '<' + man + ' ' + book + ' ' + str(num_N1) + ':' + str(num_N2) + '>'
    search_ref.append(ref)

# MorphTags
search_morph = []

for mo in GomorphTagsIds:
    search_morph.append(df_gomorphTags[df_gomorphTags['ID'] == int(mo)].iloc[0]['Name'])

#%% to DF and CSV
df_result = pd.DataFrame({'Ref': search_ref})
df_result['POS'] = TokenPOS
df_result['Morpheme'] = Morpheme
df_result['MorTag'] = search_morph
df_result['Line'] = search_line

df_result.to_csv('result_' + target_lem + '.txt', sep='\t', encoding='utf-8')
df_result.to_csv('result_' + target_lem + '.csv', sep='\t', encoding='utf-8')

#%% database to CSV - 필요할 때 주석 처리 해제하고 사용
"""df_analyses = pd.read_excel('gotica_mdb.xlsx', sheet_name='Analyses', engine='openpyxl')
print('==== Analyses sheet loading completed =====')
df_lemmata = pd.read_excel('gotica_mdb.xlsx', sheet_name='Lemmata', engine='openpyxl')
print('===== Lemmeta sheet loading completed =====')
df_gomorphTags = pd.read_excel('gotica_mdb.xlsx', sheet_name='GomorphTags', engine='openpyxl')
print('=== GomorphTags sheet loading completed ===')
df_gomorph = pd.read_excel('gotica_mdb.xlsx', sheet_name='Gomorph', engine='openpyxl')
print('===== Gomorph sheet loading completed =====')
df_pos = pd.read_excel('gotica_mdb.xlsx', sheet_name='POSTags', engine='openpyxl')
print('===== POSTags sheet loading completed =====')
df_segments = pd.read_excel('gotica_mdb.xlsx', sheet_name='Segments', engine='openpyxl')
print('==== Segments sheet loading completed =====')
df_books = pd.read_excel('gotica_mdb.xlsx', sheet_name='Books', engine='openpyxl')
print('====== Books sheet loading completed ======')
df_manuscripts = pd.read_excel('gotica_mdb.xlsx', sheet_name='Manuscripts', engine='openpyxl')
print('====== Manuscripts loading completed ======')

df_analyses.to_csv('0_Analyses.csv', encoding='utf-8')
df_lemmata.to_csv('0_Lemmata.csv', encoding='utf-8')
df_gomorphTags.to_csv('0_GomorphTags.csv', encoding='utf-8')
df_gomorph.to_csv('0_Gomorph.csv', encoding='utf-8')
df_pos.to_csv('0_POSTags.csv', encoding='utf-8')
df_segments.to_csv('0_Segments.csv', encoding='utf-8')
df_books.to_csv('0_books.csv', encoding='utf-8')
df_manuscripts.to_csv('0_Manuscripts.csv', encoding='utf-8')"""