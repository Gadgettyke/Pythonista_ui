# coding: utf-8

'''
    Pythonista .pyui files ease coding but can be difficult to post to GitHub,
    etc. so this script converts a .pyui file into a standalone .py file.

    * Ask the user to select a .pyui file
    * Create a new .py file which embeds the ui element list from .pyui file
    * Put onto the clipobard the Python code snippet to load the pyui's view
    
    my_file.py:      a user created Python script
    my_file.pyui:    a user-created file of Pythonista ui elements
    my_file_pyui.py: created by this script as a standalone .py file
                     You can run this script to fine tune the ui elements.

    This script puts a few lines of code onto the clipboard which can be
    pasted into my_file.py so that the two .py files will work together to
    load the view without requiring the .pyui file.  
    
    NOTE: Requires dialogs module that is only in Pythonista v1.6 and later
'''

import clipboard, dialogs, json, os, pprint, ui

fmt = '''# coding: utf-8

# This file was generated by pyui_embedded.py
# Source at: https://github.com/cclauss/Pythonista_ui

# See: https://omz-forums.appspot.com/pythonista/post/5254558653612032
# and: https://omz-forums.appspot.com/editorial/post/6075976853225472

import json, tempfile, ui

_ui_list = {}

def load_view_from_list(view_list=_ui_list):
    with tempfile.NamedTemporaryFile(suffix='.pyui') as temp_file:
        json.dump(view_list, temp_file)
        temp_file.seek(0)  # move the file read cursor back to byte zero
        return ui.load_view(temp_file.name)

if __name__ == '__main__':
    view = load_view_from_list(_ui_list)
    view.present(hide_title_bar=True)
'''

def get_pyui_from_user():
    pyui_files = [f for f in os.listdir(os.curdir) if f.endswith('.pyui')]
    return dialogs.list_dialog(title='Pick a file', items=pyui_files)

filename = get_pyui_from_user()
with open(filename) as in_file:
    ui_list = json.load(in_file)
filename = filename.replace('.', '_') + '.py'  # my_file.pyui --> my_file_pyui.py
with open(filename, 'w') as out_file:
    out_file.write(fmt.format(pprint.pformat(ui_list)))
clip_text = '''
import {0}
view = {0}.load_view_from_list()
view.present(hide_title_bar=True)
'''.format(filename.split('.')[0])
clipboard.set(clip_text)
print('{}\nThe clipboard now contains the code:\n{}'.format('=' * 36, clip_text))
