from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import  load_dotenv
import asyncio




import os 
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = AsyncOpenAI(api_key=OPENAI_API_KEY)



async def perform_translations(task_id:int,text:str,languages:list,db:Session):
    translations = {}

    for lang in languages:
        try:
            response = await client.chat.completions.create(model="gpt-3.5-turbo",messages=[{
                "role":"system","content":f"You are a helpful assistant that translates text in to {lang}."},
                {"role":"user","content":text}],
                max_tokens=1000
                
            )

            
            
            translated_text = response.choices[0].message.content.strip()
            translations[lang]=translated_text
        except Exception as e:
            print(f"Error translation {lang}: {e}")
        except Exception as e:
            print(f"Unexpected error:{e}")
            translations[lang]=f"Unexpected error:{e}"

            if 'insufficient_quota' in str(e):
                print("You have exceeded your quota. Please check your plan and billing details.")
                break  # Break the loop to avoid further API calls
            
        
    update_translation_task(db,task_id,translations)

 #Wrapper to run the async function in a synchronous context
def perform_translations_sync(task_id: int, text: str, languages: list, db: Session):
    asyncio.run(perform_translations(task_id, text, languages, db))
