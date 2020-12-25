import argparse
import os
import sys
from number_parser import get_number
from core import *


def check_update(local_version):
    return  # dev 跳过更新

    data = json.loads(get_html(
        "https://api.github.com/repos/yoshiko2/AV_Data_Capture/releases/latest"))

    remote = data["tag_name"]
    local = local_version

    if not local == remote:
        line1 = "* New update " + str(remote) + " *"
        print("[*]" + line1.center(54))
        print("[*]" + "↓ Download ↓".center(54))
        print("[*] https://github.com/yoshiko2/AV_Data_Capture/releases")
        print("[*]======================================================")


def argparse_function(ver: str) -> [str, str, bool]:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", default='', nargs='?',
                        help="Single Movie file path.")
    parser.add_argument("-c", "--config", default='config.ini',
                        nargs='?', help="The config file Path.")
    parser.add_argument("-n", "--number", default='',
                        nargs='?', help="Custom file number")
    parser.add_argument("-a", "--auto-exit", dest='autoexit',
                        action="store_true", help="Auto exit after program complete")
    parser.add_argument("-v", "--version", action="version", version=ver)
    args = parser.parse_args()

    return args.file, args.config, args.number, args.autoexit


def movie_lists(root, escape_folder):
    print('root is ', root)

    file_type = ['.mp4', '.avi', '.rmvb', '.wmv', '.mov', '.mkv', '.flv', '.ts', '.webm',
                 '.MP4', '.AVI', '.RMVB', '.WMV', '.MOV', '.MKV', '.FLV', '.TS', '.WEBM', '.iso', '.ISO']

    total = []

    # debug os.walk 在多目录环境下更适用
    for r, dirs, files in os.walk(root):

        def break_for():
            for e in escape_folder:
                if e in r:
                    return True

        bf = break_for()
        if bf:
            continue
        else:
            for f in files:
                f_path = os.path.join(r, f)
                if os.path.splitext(f)[1] in file_type:
                    total.append(f_path)
                else:
                    pass
    print('total files are: \n', total)
    return total


def create_failed_folder(failed_folder):
    if not os.path.exists(failed_folder + '/'):  # 新建failed文件夹
        try:
            os.makedirs(failed_folder + '/')
        except Exception as e:
            print(e)
            print(
                "[-]failed!can not be make folder 'failed'\n[-](Please run as Administrator)")
            sys.exit(0)


def CEF(path):
    try:
        files = os.listdir(path)  # 获取路径下的子文件(夹)列表
        for file in files:
            os.removedirs(path + '/' + file)  # 删除这个空文件夹
            print('[+]Deleting empty folder', path + '/' + file)
    except Exception as e:
        print(e)
        a = ''


def create_data_and_move(file_path: str, c: config.Config, debug, work_folder):
    # Normalized number, eg: 111xxx-222.mp4 -> xxx-222.mp4
    n_number = get_number(debug, file_path)

    if debug == True:
        print("[!]Making Data for [{}], the number is [{}]".format(
            file_path, n_number))
        # todo todo 更改文件名规则为 actor + num
        core_main(file_path, n_number, c, work_folder)
        print("[*]======================================================")
    else:
        try:
            print("[!]Making Data for [{}], the number is [{}]".format(
                file_path, n_number))
            core_main(file_path, n_number, c, work_folder)
            print("[*]======================================================")
        except Exception as err:
            print("[-] [{}] ERROR:".format(file_path))
            print('[-]', err)

            # 3.7.2 New: Move or not move to failed folder.

            if c.failed_move() == False:
                if c.soft_link():
                    print("[-]Link {} to failed folder".format(file_path))
                    os.symlink(file_path, str(work_folder) +
                               "/" + conf.failed_folder() + "/")
            elif c.failed_move() == True:
                if c.soft_link():
                    print("[-]Link {} to failed folder".format(file_path))
                    os.symlink(file_path, str(work_folder) +
                               "/" + conf.failed_folder() + "/")
                else:
                    try:
                        print("[-]Move [{}] to failed folder".format(file_path))
                        shutil.move(file_path, str(work_folder) +
                                    "/" + conf.failed_folder() + "/")
                    except Exception as err:
                        print('[!]', err)


def create_data_and_move_with_custom_number(file_path: str, c: config.Config, custom_number=None, work_folder='./'):
    try:
        print("[!]Making Data for [{}], the number is [{}]".format(
            file_path, custom_number))
        core_main(file_path, custom_number, c, work_folder)
        print("[*]======================================================")
    except Exception as err:
        print("[-] [{}] ERROR:".format(file_path))
        print('[-]', err)

        if c.soft_link():
            print("[-]Link {} to failed folder".format(file_path))
            os.symlink(file_path, str(work_folder) +
                       "/" + conf.failed_folder() + "/")
        else:
            try:
                print("[-]Move [{}] to failed folder".format(file_path))
                shutil.move(file_path, str(work_folder) +
                            "/" + conf.failed_folder() + "/")
            except Exception as err:
                print('[!]', err)


def main(work_folder):
    work_folder = work_folder
    version = '4.2.1'
    # Parse command line args
    single_file_path, config_file, custom_number, auto_exit = argparse_function(
        version)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config_ini = os.path.join(BASE_DIR, 'config.ini')
    # Read config.ini
    conf = config.Config(path=config_ini)

    version_print = 'Version ' + version
    print('[*]================== AV Data Capture ===================')
    print('[*]' + version_print.center(54))
    print('[*]======================================================')

    if conf.update_check():
        pass  # 禁止更新
        # check_update(version)

    create_failed_folder(conf.failed_folder())
    os.chdir(work_folder)

    # ========== Single File ==========
    if not single_file_path == '':  # single file 有问题
        print('[+]==================== Single File =====================')
        create_data_and_move_with_custom_number(
            single_file_path, conf, custom_number, work_folder)
        CEF(conf.success_folder())
        CEF(conf.failed_folder())
        print("[+]All finished!!!")
        input(
            "[+][+]Press enter key exit, you can check the error messge before you exit.")
        sys.exit(0)
    # ========== Single File ==========

    movie_list = movie_lists(
        work_folder, re.split("[,，]", conf.escape_folder()))

    count = 0
    count_all = str(len(movie_list))
    print('[+]Find', count_all, 'movies')
    if conf.debug() == True:
        print('[+]'+' DEBUG MODE ON '.center(54, '-'))
    if conf.soft_link():
        print('[!] --- Soft link mode is ENABLE! ----')
    for movie_path in movie_list:  # 遍历电影列表 交给core处理
        count = count + 1
        percentage = str(count / int(count_all) * 100)[:4] + '%'
        print('[!] - ' + percentage +
              ' [' + str(count) + '/' + count_all + '] -')
        create_data_and_move(movie_path, conf, conf.debug(), work_folder)

    CEF(conf.success_folder())
    CEF(conf.failed_folder())
    print("[+]All finished!!!")


if __name__ == '__main__':  # 外包循环 main（）
    main('E:/a')
    print('main')
    input("Press enter key exit, you can check the error message before you exit...")
    sys.exit(0)
