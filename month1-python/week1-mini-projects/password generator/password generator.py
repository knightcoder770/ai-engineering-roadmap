import string
import secrets
import random

def get_things_in_password():
    characters_list=[]
    characters=""
    while True:   
        try:
            password_length=int(input("enter the length of the password: "))
            if password_length<=0:
                print("password length must be greater than 0")
                continue
            else:
                break
        except ValueError:
            print("type only numbers to assign length of password")
            continue
    
    number=input("do you want numbers in the password?[Y/N]: ").upper()
    lower_case=input("do you want lower case letters in password?[Y/N]: ").upper()
    upper_case=input("do you want upper case letters in password? [Y/N]: ").upper()
    special_characters=input("do you want special characters in password? [Y/N]: ").upper()
       
    if number=='Y':
        characters_list.append(string.digits)
        characters+=string.digits
    if lower_case=='Y':
        characters_list.append(string.ascii_lowercase)
        characters+=string.ascii_lowercase
    if upper_case=='Y':
        characters_list.append(string.ascii_uppercase)
        characters+=string.ascii_uppercase
    if special_characters=='Y':
        characters_list.append(string.punctuation)
        characters+=string.punctuation
    
    return password_length,characters,characters_list

def generate_password(password_length,characters,characters_list):
    character=[]
    if not characters:
        print("❌ You must select at least one character type!")
        return get_things_in_password()  # restart
    for i in characters_list:
        character.append(secrets.choice(i))
    rem_length=password_length-len(character)
    for i in range (0,rem_length):
        character.append(secrets.choice(characters))
    random.shuffle(character)
        
    return "".join(character)

def password_strength(characters_list,password_length):
    if password_length<5 or len(characters_list)<2:
        return "password strength is weak"
    elif password_length>12 and len(characters_list)>=3:
        return "password is so strong but make sure you remember"
    else:
        return "password strength is good"
def main():    
    print('-'*70)
    print("let's generate your random password")
    print('-'*70)
    password_length,characters,characters_list=get_things_in_password()
    passwords=[]
    for i in range(0,5):
        password=generate_password(password_length,characters,characters_list)
        passwords.append(password)
    n=0
    for i in passwords:
        print(n+1,i)
        n+=1
    while True:   
        try:
            choosed_password=int(input("enter the number of the password you choosed from above: "))
            if choosed_password in range(1,6):
                break
        except ValueError:
            print("you must type only the number of the choosen password")
            continue
    for i in passwords:
        i=passwords[choosed_password-1]
    print(f"your new generated password is: {i}")
    print(password_strength(characters_list,password_length))
    
if __name__=="__main__":
    main()