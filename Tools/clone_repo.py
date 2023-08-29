import argparse
import os, shutil
import requests, json
import print_utils
import urllib.request, urllib.parse, urllib.error

LOGGER = print_utils.Logger()

bitbucket_user = "megaramaci2"
bitbucket_password = "FD45vdg85%"

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

def create_bitbucket_repo_v1(repo_owner, repo_name):
    url = 'https://api.bitbucket.org/1.0/repositories'
    payload = {
        'name': repo_name,
        'owner': repo_owner,
        'is_private': True,
        'no_public_forks': True
    }
    response = requests.post(url, data=urllib.parse.urlencode(payload), auth=(bitbucket_user, bitbucket_password))
    if response.status_code >= 200 and response.status_code <= 300:
        LOGGER.i("Repo %s created: %d:%s" % (repo_name, response.status_code, response.text))
        return True
    else:
        LOGGER.e("Failed to perform response (%s): %d - %s" % (url, response.status_code, response.text))
        return False

def create_bitbucket_repo_v2(repo_owner, repo_name):
    url = 'https://api.bitbucket.org/2.0/repositories/%s/%s' % (repo_owner, repo_name)
    payload = {
        'scm': "git",
        'is_private': True,
        'key' : 'PROJ',
        'fork_policy': "no_public_forks"
    }
    headers = {
        'Content-type': "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), auth=(bitbucket_user, bitbucket_password))
    if response.status_code >= 200 and response.status_code <= 300:
        LOGGER.i("Repo %s created: %d:%s" % (repo_name, response.status_code, response.text))
        return True
    else:
        LOGGER.e("Failed to perform response (%s): %d - %s" % (url, response.status_code, response.text))
        return False


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-s', '--source_repo', type=str, help="Source repository name")
    arg_parser.add_argument('-d', '--dest_repo', type=str, help="Destination repository name")
    arg_parser.add_argument('-o', '--repo_owner', type=str, default="s1teammasters", help="Bitbucket repo owner name")
    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))

    source_repo_link = "https://bitbucket.com/%s/%s.git" % (args.repo_owner, args.source_repo)
    dest_repo_link = "https://bitbucket.com/%s/%s.git" % (args.repo_owner, args.dest_repo)

    LOGGER.h("Creating repo %s" % (dest_repo_link))
    check_skip_task(create_bitbucket_repo_v2(args.repo_owner, args.dest_repo), "Failed to create repo %s. CHECK RESPONSE ERROR!!!!" % dest_repo_link)
    
    temp_path = os.path.join(script_dir, "_repo_temp")
    if os.path.exists(temp_path):
        LOGGER.w("Temporary %s already exists. Cleaning it..." % temp_path)
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)

    clone_command = "git clone --bare %s" % (source_repo_link)
    LOGGER.h("Cloning repo: %s" % (clone_command))
    os.chdir(temp_path)
    os.system(clone_command)

    mirror_command = "git push --mirror %s" % (dest_repo_link)
    LOGGER.h("Pushing new repo: %s" % (mirror_command))
    os.chdir(os.path.join(temp_path, args.source_repo + ".git"))
    os.system(mirror_command)

    LOGGER.h("Cleaning up cloned repo")
    os.chdir(os.path.join(temp_path, ".."))
    shutil.rmtree(temp_path)
