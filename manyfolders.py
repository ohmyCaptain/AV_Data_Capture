import AV_Data_Capture
import sys

folds = ['D:/a',
         'E:/a',
         '//Thinkpad-t410/d',
         '//Thinkpad-t410/e',
         '//Thinkpad-t410/f',
         '//Thinkpad-t410/j',
         '//Thinkpad-t410/g',
         ]

for f in folds:
    print('begin: ', f)
    try:
        AV_Data_Capture.main(f)
    except:
        print('Unable to connect ', f)


input("Press enter key exit, you can check the error message before you exit...")
sys.exit(0)
