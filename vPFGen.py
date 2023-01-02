import sys
import time
import json
from tkinter import filedialog
import os
from termcolor import colored
import colorama

os.system('title vPFGen')

figlet_title = '''
        ______ _______ _______              
.--.--.|   __ \    ___|     __|.-----.-----.
|  |  ||    __/    ___|    |  ||  -__|     |
 \___/ |___|  |___|   |_______||_____|__|__|
'''

colorama.init()

def cprint_info(text):
    print(colored(' INFO ', 'white', 'on_green'), text)
    return

def cprint_error(text):
    print(colored(' ERROR ', 'white', 'on_red'), text)
    return

def cprint_input(text):
    cprint_text = colored(' INFO (input) ', 'white', 'on_green')+ ' ' + text + ' :'
    return input(cprint_text)

def cprint_input_yn(text):
    cprint_text = colored(' INFO (input) ', 'white', 'on_green')+ ' ' + text + ' ' + '(' + colored(' y ', 'white', 'on_green') + ' or ' + colored(' n ', 'white', 'on_red') + ') : '
    return input(cprint_text)

print(colored(figlet_title, 'cyan'))
print(colored('Project folder creation tool for video production', 'cyan'))
print(colored('Developed by Cube\n', 'green'))

cprint_info('Please select a folder')
root_dir = filedialog.askdirectory()

if not os.path.isdir(root_dir):
    cprint_error('Folder does not exist.')
    cprint_error('Shuts down after 3 seconds.')
    time.sleep(3)
    sys.exit()

if os.listdir(root_dir):
    cprint_error('Files and folders exist in the folder.')
    cprint_error('Please select an empty folder.')
    cprint_error('Shuts down after 3 seconds.')
    time.sleep(3)
    sys.exit()

cprint_info('Please select a template json file')
template_json_dir = filedialog.askopenfilename(filetypes = [('Template','*.json')])

with open(template_json_dir, mode = 'r') as tjd:
    template_dic = json.load(tjd)

cprint_info('Use ' + colored(template_dic['name'], 'green'))

for dir_name in template_dic['dir_list']:
    cprint_info('Create ' + colored(dir_name, 'green') + ' folder')
    os.mkdir(root_dir + '/' + dir_name)

cprint_info('Construction is complete!')
cprint_info('Shuts down after 3 seconds.')
time.sleep(3)
sys.exit()
