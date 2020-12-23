import AV_Data_Capture
import sys

folds = ['C:/Users/fm117/Videos/test',
         'C:/Users/fm117/Videos/test2']

for f in folds:
    print('begin: ', f)
    AV_Data_Capture.main(f)


input("Press enter key exit, you can check the error message before you exit...")
sys.exit(0)
