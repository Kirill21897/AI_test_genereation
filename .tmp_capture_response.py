# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv(override=True)
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.prompts import SYSTEM_PROMPT, format_user_prompt
from core.models import GenerationInput
from core.generator import _get_api_base
import os

llm = ChatOpenAI(
    openai_api_base=_get_api_base(),
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    model=os.getenv('MAIN_MODEL').split(',')[0].strip(),
    temperature=0.7,
    request_timeout=30,
    max_retries=0,
)
input_data = GenerationInput(topic='Контроль скважины', specialty='Инженер по бурению', level='Senior', num_questions=3)
messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=format_user_prompt(input_data, 'Нет дополнительного контекста.') + '\n\nВерни ответ строго в формате JSON без дополнительного текста.')
]
response = llm.invoke(messages)
content = response.content if isinstance(response.content, str) else str(response.content)
with open('.dbg\\raw-main-response.json', 'w', encoding='utf-8') as f:
    f.write(content)
print('saved')