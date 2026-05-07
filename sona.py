import json, random, logging

logging.basicConfig(filename='sona.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)',datefmt="%m/%d/%Y %I%S %p", filemode='w')

global default_chat_data # sonady_data.json에 포함되지 않은 미리 추가할 단어를 넣어두는 dict 입니다.
global failure_chat_text # study.study() 에서 예외(ex: @등 금지 단어 포함, 한 keyword당 포함될 수 있는 description 개수 초과등)
global max_study_count # 한 keyword 당 포함될 수 있는 최대 description 개수 입니다.
global study_return_format
global study_return_format_data

class study():
    # 저장된 챗봇 데이터를 불러옵니다. 이 함수를 통한 접근을 추천하지 않습니다.
    def load():
        try:
            with open('sonady_data.json', 'r', encoding='UTF-8') as f:return json.load(f)
        except FileNotFoundError:return {}
    
    # 챗봇 데이터를 저장합니다. 이 함수를 통한 접근을 추천하지 않습니다.
    def save(chat):
        with open('sonady_data.json', 'w', encoding='UTF-8') as f:json.dump(chat, f)

    # 챗봇 데이터에 단어와 설명을 추가합니다.
    def study(keyword: str, description: str, user_id: int, user_name: str):
        chat=study.load()
        if '@' in description or 'https://' in description or 'http://' in description or 'discord.gg' in description or 'discord.com' in description or keyword in default_chat_data_keys:
            return failure_chat_text
        if keyword not in chat:chat[keyword]=[]
        if len(chat[keyword]) < max_study_count:
            chat[keyword].append(
                {
                    'description': description,
                    'user_id': user_id,
                    'user_display': user_name,
                }
            )
            study.save(chat_data)
        else:return failure_chat_text

    def delete_keyword(keyword: str, index: int):
        chat=study.load()
        if len(chat[keyword])<index:
            del chat[keyword][index]
            return f'{keyword}의 {index}번째 항목을 삭제하였습니다.'
        else:return '삭제할 항목이 존재하지 않습니다.'

    def get(keyword):
        if keyword in default_chat_data:
            return  
