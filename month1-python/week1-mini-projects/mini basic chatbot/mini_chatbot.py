import json
import os
import random
from datetime import datetime

def load_json():
    base_dir = r"F:\ai engineer\python fundamentals\mini basic chatbot"
    file_path = os.path.join(base_dir, "mini chatbot.json")
    if os.path.exists(file_path):
        with open(file_path,"r") as file:
            try:
                data=json.load(file)
                return data
            except Exception as e:
                print(e)
    else:
        print("File not found")
        return None

def save_chat(user_input, output):
    base_dir = r"F:\ai engineer\python fundamentals\mini basic chatbot"
    file_path = os.path.join(base_dir, "chat_log.json")

    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user input": user_input,
        "output": output
    }

    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except:
            data = []
    else:
        data = []
    data.append(new_entry)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        
def get_intent(intent,user_input):
    
    for intent_name, intent_data in intent.items():
        for pattern in intent_data['pattern']:
            ai_words = pattern.lower().split()

            for word in user_input:
                if word in ai_words:
                    output = random.choice(intent_data['response'])
                    return output
    print("still i am in development stage so i couldn't understand")
    
def main():
    print(os.getcwd())
    intent=load_json()
    print('-'*100)
    print('*'*20,"BASIC AI CHATBOT",'*'*20)
    print('-'*100)
    while True:    
        user_input=input("text something or q to quit: ").lower().strip()
        if user_input=='q':
            break
        else:
            user_input=user_input.split()
            output=get_intent(intent,user_input)
            print(output)
            save_chat(user_input,output)

if __name__== "__main__":
    main()