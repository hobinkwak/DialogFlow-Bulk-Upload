import os
import json
import pandas as pd

class DialogFlow:

    def __init__(self, topicid, topic, qaid, question, answer):

        self.topicid = topicid
        self.topic = topic
        self.qaid = qaid
        self.question = question
        self.answer = answer

    def __str__(self):
        return "질문: " + self.question + "\n답변: " + self.answer + "\n"


def read_csv(path='data/sample_qa.csv'):
    dataset = pd.read_csv(path)[['Topic_Id','Topic','QA_Id','질문','답변']]
    df = pd.DataFrame()
    for key, data in dataset.groupby('Topic'):
        tmp = data.copy()
        tmp['QA_Id'] = pd.factorize(tmp.답변)[0] + 1
        df = pd.concat([df, tmp])
    df = df.sort_index()
    return df


def make_conversations(df):        
    conversations = []
    for row in df.values:
        r = DialogFlow(row[0], row[1], row[2], row[3], row[4])
        conversations.append(r)
    return conversations

def make_json(conversations):
    os.makedirs('agent', exist_ok=True)
    os.chdir('agent')

    f = open('agent.json',  'w', encoding='UTF-8')
    f.write('{"language": "ko", "defaultTimezone": "Asia/Tokyo"}')
    f.close()

    f = open('package.json',  'w', encoding='UTF-8')
    f.write('{"version":"1.0.0"}')
    f.close()

    os.makedirs('intents', exist_ok=True)
    os.chdir('intents')

    for idx, c in enumerate(conversations):
        if idx == 0:

            filename = str(c.topicid) + '_' + str(c.qaid)
            name = str(c.topicid).zfill(2) + '_' + str(c.topic) + '_' +  str(c.qaid).zfill(2)
            topicid = c.topicid
            qaid = c.qaid
            with open(f"{filename}.json", 'w') as outfile:
                data = {
                "name": name,
                "auto": True,
                "contexts": [],
                "responses": [{
                    "resetContexts": False,
                    "action": "",
                    "messages": [{
                        "type": 0,
                        "lang": "ko",
                        "speech": [
                            c.answer
                        ]
                    }],
                    "affectedContexts": []
                }]
            }
                json.dump(data, outfile)

            f = open(filename + '_usersays_ko.json',  'w', encoding='UTF-8')

            f.write("[")
            f.write('{"isTemplate": false, "count": 0, "updated": 0, "lang": "ko", "data": [{"text": "' +
                c.question + '", "userDefined": false}]}')
            continue

        while True:
            if topicid != c.topicid:
                f.write("]")
                f.close()

                filename = str(c.topicid) + '_' + str(c.qaid)
                name = str(c.topicid).zfill(2) + '_' + str(c.topic) + '_' +  str(c.qaid).zfill(2)
                topicid = c.topicid
                qaid = c.qaid
                with open(f"{filename}.json", 'w') as outfile:
                    data = {
                    "name": name,
                    "auto": True,
                    "contexts": [],
                    "responses": [{
                        "resetContexts": False,
                        "action": "",
                        "messages": [{
                            "type": 0,
                            "lang": "ko",
                            "speech": [
                                c.answer
                            ]
                        }],
                        "affectedContexts": []
                    }]
                }
                    json.dump(data, outfile)

                f = open(filename + '_usersays_ko.json',  'w', encoding='UTF-8')

                f.write("[")
                f.write('{"isTemplate": false, "count": 0, "updated": 0, "lang": "ko", "data": [{"text": "' +
                c.question + '", "userDefined": false}]}')

                break
            elif topicid == c.topicid:
                if qaid == c.qaid:
                    f.write(',')
                    f.write('{"isTemplate": false, "count": 0, "updated": 0, "lang": "ko", "data": [{"text": "' +
                    c.question + '", "userDefined": false}]}')

                elif qaid != c.qaid:
                    f.write("]")
                    f.close()

                    filename = str(c.topicid) + '_' + str(c.qaid)
                    name = str(c.topicid).zfill(2) + '_' + str(c.topic) + '_' +  str(c.qaid).zfill(2)
                    topicid = c.topicid
                    qaid = c.qaid
                    with open(f"{filename}.json", 'w') as outfile:
                        data = {
                            "name": name,
                            "auto": True,
                            "contexts": [],
                            "responses": [{
                                "resetContexts": False,
                                "action": "",
                                "messages": [{
                                    "type": 0,
                                    "lang": "ko",
                                    "speech": [
                                        c.answer
                                    ]
                                }],
                                "affectedContexts": []
                            }]
                        }
                        json.dump(data, outfile)

                    f = open(filename + '_usersays_ko.json',  'w', encoding='UTF-8')

                    f.write("[")
                    f.write('{"isTemplate": false, "count": 0, "updated": 0, "lang": "ko", "data": [{"text": "' +
                    c.question + '", "userDefined": false}]}')

                break
        if idx == len(conversations)-1:
            f.write("]")
            f.close()
    os.chdir('../..')
            
            
if __name__ == '__main__':
    df = read_csv()
    conversations = make_conversations()
    make_json(conversations)