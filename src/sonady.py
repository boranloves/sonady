import json, random, logging

logging.basicConfig(filename='sonady.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)',datefmt="%m/%d/%Y %I%S %p", filemode='w')

global failure_chat_text_r # study.study() 에서 예외(ex: @등 금지 단어 포함, 한 keyword당 포함될 수 있는 description 개수 초과등)
global max_study_count_r # 한 keyword 당 포함될 수 있는 최대 description 개수 입니다.
global study_return_format_r # study.study()가 정상 수행된 후 return 하는 str의 포멧을 설정합니다.
global study_return_format_data_r
global study_ban_word

failure_chat_text_r=''
max_study_count_r=0
study_return_format_r=''
study_return_format_data_r=''
study_ban_word=set()

class study():
    # sonady 사용전 설정해야 할 옵션을 설정합니다.
    def lunch(failure_chat_text='', max_study_count=3, study_return_format='', study_return_format_data='', study_ban_word: set=set()):
        failure_chat_text_r=failure_chat_text
        max_study_count_r=max_study_count
        study_return_format_r=study_return_format
        study_return_format_data_r=study_return_format_data
        logging.debug('sonady was lunched')
        
    # 저장된 챗봇 데이터를 불러옵니다. 이 함수를 통한 접근을 추천하지 않습니다.
    def load():
        try:
            with open('sonady_data.json', 'r', encoding='UTF-8') as f:logging.debug('load to chat database flie');return json.load(f)
        except FileNotFoundError:return {}
    
    # 챗봇 데이터를 저장합니다. 이 함수를 통한 접근을 추천하지 않습니다.
    def save(chat):
        with open('sonady_data.json', 'w', encoding='UTF-8') as f:logging.debug('save to chat database flie');json.dump(chat, f)

    # 챗봇 데이터에 단어와 설명을 추가합니다.
    def study(keyword: str, description: str, user_id: int, user_name: str):
        chat=study.load()
        if '@' in description or 'https://' in description or 'http://' in description or 'discord.gg' in description or 'discord.com' in description:
            return failure_chat_text_r
        if keyword not in chat:chat[keyword]=[]
        if len(chat[keyword]) < max_study_count_r:
            chat[keyword].append(
                {
                    'description': description,
                    'user_id': user_id,
                    'user_display': user_name,
                }
            )
            study.save(chat)
        else:return failure_chat_text_r

    # 챗봇 데이터에 존제하는 keyword의 index번째 항목을 삭제합니다. 없을 경우 -를 return 합니다. 또한 index는 python의 인덱스방식을 따릅니다(0부터 시작)
    def delete_keyword(keyword: str, index: int):
        chat=study.load()
        if len(chat[keyword])<index:
            del chat[keyword][index]
            return f'{keyword}의 {index}번째 항목을 삭제하였습니다.'
        else:return '삭제할 항목이 존재하지 않습니다.'
    
    # 챗봇 데이터에서 keyword의 임의의 description와 user_display, user_id를 tuple로 return 합니다.
    def get(keyword):
        chat=study.load()
        if keyword in chat:
            idx=random.randint(0,len(chat[keyword]))
            return chat[keyword][idx]['description'], chat[keyword][idx]['user_display'], chat[keyword][idx]['user_id']
        else:
            return None, None, None
