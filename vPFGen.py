import os
import json
import questionary
import tkinter as tk
from tkinter import filedialog
import sys
import time
from termcolor import colored
import colorama

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

def create_folders_from_json(data, base_path, target_folder_origin):
    """
    JSONの構造に基づいてフォルダ階層を作成する関数。

    :param data: JSONデータ (辞書形式)
    :param base_path: フォルダを作成する基準となるパス
    """
    base_path_origin = target_folder_origin

    for key, value in data.items():
        folder_path = os.path.join(base_path, key)
        os.makedirs(folder_path, exist_ok=True)
        cprint_info('Create ' + colored(folder_path.replace(base_path_origin,''), 'green') + ' folder')
        if isinstance(value, dict):
            create_folders_from_json(value, folder_path, base_path_origin)

def select_folder():
    """
    フォルダ選択ダイアログを表示する。
    :return: 選択したフォルダのパス
    """
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする
    folder_path = filedialog.askdirectory(title="フォルダを選択してください")
    return folder_path

def list_templates(template_dir):
    """
    テンプレートフォルダ内のJSONファイルを一覧取得する。
    :param template_dir: テンプレートフォルダのパス
    :return: JSONファイルのリスト
    """
    return [f for f in os.listdir(template_dir) if f.endswith('.json')]

def main():

    os.system('title vPFGen')

    figlet_title = '''
            ______ _______ _______              
    .--.--.|   __ \    ___|     __|.-----.-----.
    |  |  ||    __/    ___|    |  ||  -__|     |
    \___/ |___|  |___|   |_______||_____|__|__|
    '''

    colorama.init()

    print(colored(figlet_title, 'cyan'))
    print(colored('Project folder creation tool', 'cyan'))
    print(colored('Developed by Cube\n', 'green'))

    cprint_info('Please select a folder')

    # テンプレートフォルダ（スクリプトと同じディレクトリ内にある "templates" フォルダ）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, "templates")
    
    # テンプレートファイルの一覧を取得
    templates = list_templates(template_dir)
    if not templates:
        print('Template not found. Please prepare a JSON file in the "templates" folder.')
        return
    
    # questionaryでテンプレートを選択
    cprint_info('Please select a template json file')
    selected_template = questionary.select(
        "",
        choices=templates
    ).ask()
    
    if not selected_template:
        print("No template was selected.")
        return

    template_path = os.path.join(template_dir, selected_template)

    # JSONファイルを読み込む
    with open(template_path, 'r') as file:
        data = json.load(file)

    # テンプレート情報を取得
    template_name = data.get("template_name", "UnnamedTemplate")
    description = data.get("description", "No description provided")
    folder_structure = data.get("structure", {})

    cprint_info('Use ' + colored(template_name, 'green'))
    cprint_info('Use ' + colored(description, 'green'))

    # フォルダ選択ダイアログを表示
    cprint_info('Please select a root folder')
    target_folder = select_folder()
    if not target_folder:
        print("No folder was selected.")
        return

    if not os.path.isdir(target_folder):
        cprint_error('Folder does not exist.')
        cprint_error('Shuts down after 3 seconds.')
        time.sleep(3)
        sys.exit()

    if os.listdir(target_folder):
        cprint_error('Files and folders exist in the folder.')
        cprint_error('Please select an empty folder.')
        cprint_error('Shuts down after 3 seconds.')
        time.sleep(3)
        sys.exit()

    # フォルダを作成
    create_folders_from_json(folder_structure, target_folder, target_folder)
    cprint_info('Construction is complete!')
    cprint_info('Shuts down after 3 seconds.')
    time.sleep(3)
    sys.exit()

if __name__ == "__main__":
    main()