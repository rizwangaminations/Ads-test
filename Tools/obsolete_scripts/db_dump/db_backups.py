import subprocess
import os
import zipfile
import shutil
from pprint import pprint

IGNORED_FILES = ['desktop.ini', 'thumbs.db', '.ds_store',
                 'icon\r', '.dropbox', '.dropbox.attr']

def is_ignored(filename):
    filename_lower = filename.lower()
    for ignored_file in IGNORED_FILES:
        if ignored_file in filename_lower:
            return True
    return False

def main():
    newEngineApps={
            "NE-11": "mongodb://heroku_2814xx5x:2svc7tfffm2okiqn432d3crla9@ds161495.mlab.com:61495/heroku_2814xx5x",
            "NE-12": "mongodb://heroku_jjfnhlmc:r897846d26m8sun31ietoads0a@ds161495.mlab.com:61495/heroku_jjfnhlmc",
            "NE-13": "mongodb://heroku_0g0bh5rz:57vh816v5sbgvv10o89aspq5k8@ds023684.mlab.com:23684/heroku_0g0bh5rz",
            "NE-14": "mongodb://heroku_dqdwkw1g:td9qptb8tk78m0c73g3ja5hnjb@ds017896.mlab.com:17896/heroku_dqdwkw1g",
            "NE-15": "mongodb://heroku_zt3jx8r5:k7o6o0v5rdgcomieverf5ri9co@ds019076.mlab.com:19076/heroku_zt3jx8r5",
            "NE-16": "mongodb://heroku_0rf88ltp:k37h1hc71bp09jdff3hvutkpqr@ds019936.mlab.com:19936/heroku_0rf88ltp",
            "NE-17": "mongodb://heroku_bn776j54:ff785g8ujk3j1nhgaa5oi6764h@ds019816.mlab.com:19816/heroku_bn776j54",
            "NE-18": "mongodb://heroku_sgqh7jzx:nkqg22kskl6jsc3dptjuhapdoj@ds019876.mlab.com:19876/heroku_sgqh7jzx",
            "NE-19": "mongodb://heroku_sxh2z1x5:jd2ic7htbhikk9e9gm4qa27f9b@ds033116.mlab.com:33116/heroku_sxh2z1x5",
            "NE-20": "mongodb://heroku_4951tk6r:eqkpi4t18jt4le31kghqtpiofc@ds033116.mlab.com:33116/heroku_4951tk6r",
            "NE-21": "mongodb://heroku_8jd2dkhr:38abr868uvif3lf2v0cp1meov6@ds033036.mlab.com:33036/heroku_8jd2dkhr",
            "NE-22": "mongodb://heroku_cw52lp9k:lg856mbo8e44hmokifucfhobm8@ds041536.mlab.com:41536/heroku_cw52lp9k",
            "NE-23": "mongodb://heroku_bcs8xzjg:1ojtokemnih1cscodo6fmlaor8@ds041536.mlab.com:41536/heroku_bcs8xzjg",
            "NE-24": "mongodb://heroku_4tz28mbs:8hn8s3k04ah6c3k61u43dq11q@ds047166.mlab.com:47166/heroku_4tz28mbs",
            "NE-25": "mongodb://heroku_47x97lqk:hhjojqtl2rsoh6mnpnqd5hot7r@ds049466.mlab.com:49466/heroku_47x97lqk",
            "NE-26": "mongodb://heroku_cgw1brkr:do1aqc1p716qdeo6vjqpkfac09@ds053216.mlab.com:53216/heroku_cgw1brkr",
            "NE-27": "mongodb://heroku_gzpvq4p6:7cda3ugv9u34j2ao2njas8sq6u@ds039020.mlab.com:39020/heroku_gzpvq4p6",
            "NE-28": "mongodb://heroku_n7kqxdq3:g4mts5ir8tc6360tmbh6l8f93b@ds059496.mlab.com:59496/heroku_n7kqxdq3",
            "NE-29": "mongodb://heroku_058v80zt:he6ed87prnd77ladf3822gfvlj@ds063546.mlab.com:63546/heroku_058v80zt",
            "NE-30": "mongodb://heroku_vt8w3hvm:eka97u33e5ia2kik8mg8hnuvfb@ds031167.mlab.com:31167/heroku_vt8w3hvm",
            "NE-31": "mongodb://heroku_4486gfrz:h6mqmsjujvk8rt2l5bics5hner@ds035177.mlab.com:35177/heroku_4486gfrz",
            "NE-32": "mongodb://heroku_4rwshwsk:7adtdf0j1h79lagkdosg3s82tf@ds021299.mlab.com:21299/heroku_4rwshwsk",
            "NE-33": "mongodb://heroku_2fmbgv74:d3cdkqhsjvuq8ubbohmor61oj6@ds161497.mlab.com:61497/heroku_2fmbgv74",
            "NE-34": "mongodb://heroku_7jm9h0xd:g7dod38og4adbmegdn80aho60v@ds113668.mlab.com:13668/heroku_7jm9h0xd",
            "NE-35": "mongodb://heroku_g7lfvhxh:trel7aacph50v698gd15gtu8he@ds133378.mlab.com:33378/heroku_g7lfvhxh",
            "NE-36": "mongodb://heroku_38kx11ks:7e1pf7sdt0arf4ivudldrp0j2e@ds151018.mlab.com:51018/heroku_38kx11ks",
            "NE-37": "mongodb://heroku_tk6bv92b:scf1qu3k57jd5nn4i83q482o4q@ds117869.mlab.com:17869/heroku_tk6bv92b",
            "NE-38": "mongodb://heroku_8gc5936r:39qn8us4u0vissutvmcdtkfmle@ds137139.mlab.com:37139/heroku_8gc5936r",
            "NE-43": "mongodb://heroku_bvbpd2w5:5idsjjrpv9n576u9bps2ebqsp1@ds139277.mlab.com:39277/heroku_bvbpd2w5",
            "NE-45": "mongodb://heroku_fs2ps380:iju5bbidj1c778g68u73tt1c2m@ds035703.mlab.com:35703/heroku_fs2ps380",
            "NE-46": "mongodb://heroku_s4x4nwf8:uilfupp35brbed41qcb3k5npl0@ds127300.mlab.com:27300/heroku_s4x4nwf8",
            "IL-1": "mongodb://heroku_jn521fw5:sloo5623llpeq64navq1647c6u@ds137491-a0.mlab.com:37491/heroku_jn521fw5",
            "IL-2": "mongodb://heroku_fn49vxsz:u80or3t3o9423n50o9vdpu7shs@ds157681-a0.mlab.com:57681/heroku_fn49vxsz",
            "IL-3": "mongodb://heroku_2h542nt8:73g02bscqtfdgqqrkqpgddfvkq@ds141792-a0.mlab.com:41792/heroku_2h542nt8",
            "IL-4": "mongodb://heroku_1h4klf2q:a0tbsb9cla5rrbeljug3d3fqlo@ds155532-a0.mlab.com:55532/heroku_1h4klf2q",
            "IL-5": "mongodb://heroku_n1tcs5tn:sb9ol883v9rncghel8684op96l@ds127543-a0.mlab.com:27543/heroku_n1tcs5tn",
            "MG-1": "mongodb://heroku_hzqmqj3h:1gnen4fao8munkd77vkpg7lora@ds127949.mlab.com:27949/heroku_hzqmqj3h",
            "MG-2": "mongodb://heroku_8hm0dnpz:2tuhmojt4r52hgvupdv7ck6sc1@ds159998.mlab.com:59998/heroku_8hm0dnpz",
            "MG-3": "mongodb://heroku_pdsd13bx:m2d7co0o28f8vi0pta2f391nmi@ds119788.mlab.com:19788/heroku_pdsd13bx"}

    try:
        os.remove(os.path.dirname(os.path.abspath(__file__)) + "/Dump_Process_Log_File.txt")
        os.remove(os.path.dirname(os.path.abspath(__file__)) + "/Error.txt")
    except:
        pass
        
    for key in list(newEngineApps.keys()):
        print("Dumping dbData for", key)
        userName = newEngineApps[key].split('//')[1].split(':')[0]
        password = newEngineApps[key].split(':')[2].split('@')[0]
        URI = newEngineApps[key].split('/')[2].split('@')[1]
        NEAppName = key
            
        params_by_env = {}

        # "inherit" the current environment
        for k,v in list(os.environ.items()):
            params_by_env[k] = v
        # Specify the envvars for export_db.bat file
        params_by_env['USER_NAME'] = userName
        params_by_env['PASSWORD'] = password
        params_by_env['URI'] = URI
        params_by_env['APP'] = NEAppName

        filepath=os.path.dirname(os.path.abspath(__file__)) + "\export_db.bat"
        p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE, env=params_by_env)
        p.wait()
            
        # compressing a folder
        # src=os.path.dirname(os.path.abspath(__file__)) + "/dump/" + key
        # compressFolder(src,src)
            
        # deleting the folder
        # deleteFolder(src)

    
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/Dump_Process_Log_File.txt"
    file = open(filepath,'w')
    file.write('/////////// Starting logs for db backups//////////')

    totalNEApps = len (newEngineApps)
    notBackedUpAppsCount = checkTotalBackupFolder(totalNEApps);
    file.write('\nBackups: Not Backedup apps count %s' % (notBackedUpAppsCount))
    file.close()

def checkTotalBackupFolder(totalNEApps):

    filepath = os.path.dirname(os.path.abspath(__file__)) + "/Dump_Process_Log_File.txt"
    errorFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Error.txt"

    dumpFolderPath = os.path.dirname(os.path.abspath(__file__)) + "/dump"
    backedupNEApps = 0

    for filename in os.listdir(dumpFolderPath):
        if is_ignored(filename):
            continue
        else:
            backedupNEApps+=1
    if backedupNEApps != totalNEApps:
        error = open(errorFilePath,'w')
        error.close()
    return totalNEApps-backedupNEApps


def compressFolder(src, dst):
    print("Starting to zip", src)
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zf.write(absname, arcname)
    zf.close()

def deleteFolder(src):
    print("deleting", src)
    shutil.rmtree(src, ignore_errors=False, onerror=None)

main()
