necessary steps:
Install:
1. pip install PyQt5
2. pip install pyqt5designer

* QT Designer can be executed from the CMD executing the command 'designer'
* You can also find the .exe in directory like this: C:\Users\[user]\AppData\Local\Programs\Python\[yourPythonVer]\Lib\site-packages\QtDesigner
Example:
C:\Users\Carlos\AppData\Local\Programs\Python\Python311\Lib\site-packages\QtDesigner

* Build a window and save it
* it will be a file .ui as result.
* You can transform it into a python file by executing the command: pyuic5 -x test.ui -o test.py
