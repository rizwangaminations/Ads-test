import os, sys
import subprocess
import shutil
import stat
import print_utils

def run_py(script, *args):
    args_list = ['python', script]
    for arg in args:
        args_list.append(arg)
    subprocess.Popen(args_list).communicate()

def check_skip_task(result, skip_message):
    if result == True:
        return True
    answer = input("%s. Continue? Y/N: " % skip_message)
    if answer in ["Yes", "YES", "yes", "Y", "y"]:
        return True
    elif answer in ["No", "NO", "no", "N", "n"]:
        exit(0)
    else:
        return check_skip_task(result, skip_message)

def join_path(*args):
    return os.path.normpath(os.path.join(*args))

def get_env(key, default_value=None):
    return os.environ.get(key, default_value)

def get_n_cpus():
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except:
        pass
    return 1

def run_command(command, working_dir = None, exit_on_fail = True):
    ret = subprocess.call(command, shell=True, cwd=working_dir)
    if ret != 0 and exit_on_fail == True:
        error_msg = "Error executing command %s\nERROR CODE %d" % (command, ret)
        raise Exception(print_utils.ColoredString(error_msg, print_utils.bcolors.FAIL))
        exit(ret)
    return ret

def copytree(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def remove_tree(path, skip_errors = True):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors = skip_errors)
