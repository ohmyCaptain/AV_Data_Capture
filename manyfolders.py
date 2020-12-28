import AV_Data_Capture
import sys
import os

folds = [
    'D:/a',
    'E:/a',
    '//Thinkpad-t410/d',
    '//Thinkpad-t410/e',
    '//Thinkpad-t410/f',
    '//Thinkpad-t410/j',
    '//Thinkpad-t410/g',
    '//192.168.88.18/a/qbt/downloads/jav/done/归类完成',
    'C:/Users/fm117/Downloads/bt'
]

for f in folds:
    if os.path.exists(f):
        print('begin: ', f)
        AV_Data_Capture.main(f)
    else:
        print('Unable to connect ', f)


input("Press enter key exit, you can check the error message before you exit...")
sys.exit(0)
