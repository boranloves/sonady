import json, random, logging

logging.basicConfig(filename='sonady.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)',datefmt="%m/%d/%Y %I%S %p", filemode='w')

global failure_chat_text_r # study.study() 에서 예외(ex: @등 금지 단어 포함, 한 keyword당 포함될 수 있는 description 개수 초과등)
global max_study_count_r # 한 keyword 당 포함될 수 있는 최대 description 개수 입니다.
global study_return_format_r # study.study()가 정상 수행된 후 return 하는 str의 포멧을 설정합니다.
global study_return_format_data_r
global study_ban_word_r

failure_chat_text_r=''
max_study_count_r=0
study_return_format_r=''
study_ban_word_r=[]

''' sonady 사용전 설정해야 할 옵션을 설정합니다.'''
def lunch(failure_chat_text='', max_study_count=3, study_return_format='', study_ban_word: list=[]):
    '''sonady 실행전 필요한 함수값을 정의 합니다.
    
    Args:
        failure_chat_text (str): sonady.study에서 keyword와 description에 문제가 있는 경우 return 합니다. 
        max_study_count (int): sonady.study에서 같은 keyword 당 최대로 가질 수 있는 description의 개수를 정의합니다. 기본값은 3입니다.
        study_return_format (str): sonady.say에서 return되는 추가 정보들의 형식을 지정합니다. user_id를 사용하려면 *user_id*, display_name을 사용하려면 *display_name*을 문자열에 넣으십시오.
        study_ban_word (list): sonady.study에서 필터링하고 싶은 내용을 넣어 keyword나 description에 포함되어 있을시 failure_chat_text를 return 시키게 합니다.

    Return:
        Return값은 없습니다.
    '''
    failure_chat_text_r=failure_chat_text
    max_study_count_r=max_study_count
    study_return_format_r=study_return_format
    study_ban_word_r=study_ban_word
    logging.debug('sonady was lunched')
    
'''# 저장된 챗봇 데이터를 불러옵니다. 이 함수를 통한 접근을 추천하지 않습니다.'''
def study_load():
    try:
        with open('sonady_data.json', 'r', encoding='UTF-8') as f:logging.debug('load to chat database flie');return json.load(f)
    except FileNotFoundError:return {}
    
# 챗봇 데이터를 저장합니다. 이 함수를 통한 접근을 추천하지 않습니다.
def study_save(chat):
    with open('sonady_data.json', 'w', encoding='UTF-8') as f:logging.debug('save to chat database flie');json.dump(chat, f)

# 챗봇 데이터에 단어와 설명을 추가합니다.
def study(keyword: str, description: str, user_id: int, user_name: str):
    '''단어와 설명을 입력받아 데이터베이스에 저장합니다.
    Args:
        keyword (str):sonadt.say에서 keyword를  
    '''
    chat=study.load()
    for p in study_ban_word_r:
        if p in keyword or p in description:
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
        study_save(chat)
    else:return failure_chat_text_r

# 챗봇 데이터에 존제하는 keyword의 index번째 항목을 삭제합니다. 없을 경우 -를 return 합니다. 또한 index는 python의 인덱스방식을 따릅니다(0부터 시작)
def delete_keyword(keyword: str, index: int):
    chat=study.load()
    if len(chat[keyword])<index:
        del chat[keyword][index]
        return f'{keyword}의 {index}번째 항목을 삭제하였습니다.'
    else:return '삭제할 항목이 존재하지 않습니다.'
    
# 챗봇 데이터에서 keyword의 임의의 description와 user_display, user_id를 tuple로 return 합니다.
def say(keyword):
    chat=study.load()
    if keyword in chat:
        idx=random.randint(0,len(chat[keyword]))
        return chat[keyword][idx]['description'], chat[keyword][idx]['user_display'], chat[keyword][idx]['user_id']
    else:
        return None, None, None
