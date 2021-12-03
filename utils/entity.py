import os
import json
import  re
from glob import glob

class EntityCatcher:
    
    def __init__(self, entity_path='agent/entities', intents_path='agent/intents'):
        self.entity_path = glob(entity_path + '/*ko.json')
        self.intents_path = glob(intents_path + '/*')
        self.entity_dic = None
        self.entity_naive = None
        self.entity_list = None
        self.pattern = None
        
    def _make_entity_dic(self):
        entity_dic = {}
        for file in self.entity_path:
            entities = json.load(open(file, 'r' , encoding='UTF-8'))
            entity_dic[os.path.basename(file).split('_entries_')[0]] = {}
            for entity in entities:
                entity_dic[os.path.basename(file).split('_entries_')[0]][entity['value']] = entity['synonyms']
        self.entity_dic = entity_dic
        return self.entity_dic
        
        
    def _make_entity_naive(self):
        entity_naive = {}
        for key in self.entity_dic:
            entity_naive[key] = []
            for k in self.entity_dic[key]:
                entity_naive[key].extend(self.entity_dic[key][k])
        self.entity_naive = entity_naive
        return self.entity_naive
    
    
    def _make_entity_list(self):
        entity_list = []
        for key in self.entity_naive:
            entity_list.extend(self.entity_naive[key])
        entity_list = sorted(entity_list, key=lambda x: len(x), reverse=True)
        self.entity_list = entity_list
        return entity_list
        
        
    def _make_pattern(self):
        pattern = '|'.join(self.entity_list)
        pattern = pattern.replace('(', '\(')
        pattern = pattern.replace(')', '\)')
        self.pattern = pattern
        return self.pattern

    def make_param(self):
        self._make_entity_dic()
        self._make_entity_naive()
        self._make_entity_list()
        self._make_pattern()
    
    
    def catch_entity(self, data):
        self.make_param()
        old_text = ''.join([dic['text'] for dic in data])
        new_data = []
        entity = re.findall(self.pattern, old_text)
        if len(entity) == 0 :
            return data
        text = old_text
        tmp = []

        while True:
            search = re.search(self.pattern, text)
            if search == None:
                break
            idx_s, idx_e = search.span()
            adj = len(old_text) - len(text)
            text = text[idx_e:]
            idx_s += adj
            idx_e += adj
            tmp.append((idx_s, idx_e))

        index = [0]
        for tup in tmp:
            index.append(tup[0])
            index.append(tup[1])
        parts = [old_text[i:j] for i,j in zip(index, index[1:]+[None])]


        for part in parts:
            if part in entity:
                for key in self.entity_naive:
                    if part in self.entity_naive[key]:
                        tag = key[0].upper() + key[1:]
                new_data.append({'text': part, 'meta': f'@{tag}', 'alias': f'{tag}', 'userDefined': True})
            else:
                new_data.append({'text': part, 'userDefined': False})

        return new_data
    
    def entity_to_quetion(self):
        for file in self.intents_path:
            if file.find('usersays') >= 0 :
                question = json.load(open(file, 'r', encoding='UTF-8'))
                data = []
                for q in question:
                    q['data'] = self.catch_entity(q['data'])
                    data.append(q)
                json.dump(data, open(file, 'w', encoding='UTF-8'))
                
    def initialize_answer(self):
        for file in self.intents_path:
            if file.find('usersays') < 0 :
                answer = json.load(open(file, 'r', encoding='UTF-8'))
                answer['responses'][0]['parameters'] = []
                json.dump(answer, open(file, 'w', encoding='UTF-8'))
            
    