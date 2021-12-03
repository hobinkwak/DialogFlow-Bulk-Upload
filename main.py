from utils.upload import *
from utils.entity import *

def main(generate_intents=True, catch_entity=True):
    if generate_intents:
        df = read_csv()
        conversations = make_conversations(df)
        make_json(conversations)
        
    if catch_entity:
        ec = EntityCatcher()
        ec.entity_to_quetion()
        ec.initialize_answer()
        
if __name__ == '__main__':
    # csv로부터 intents json 생성
    main(generate_intents=True, catch_entity=False)
    # entity 파일이 있다는 전제하에
    main(generate_intents=False, catch_entity=True)