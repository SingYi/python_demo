#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands
import os,sys
import plistlib
import zipfile
import shutil
import re

reload(sys) 
sys.setdefaultencoding('utf-8')

__autor__ = "Sans"
_private_security                   = "/usr/bin/security"
_private_sign_file_type = ['.framework','.dylib','.app']

_private_Provisioning_profiles_path = "Library/MobileDevice/Provisioning Profiles"
_private_shell_pp_path              = "Library/MobileDevice/Provisioning\ Profiles"
_private_tmp_path                   = '/tmp/resign_app'
_un_zip_path                        = _private_tmp_path + '/unzip'
_resign_tmp_path                    = _private_tmp_path + '/resign'
_resign_Pay_load_path               = _resign_tmp_path + '/Payload'

_private_resign_info = {
    '_private_code_sign_app_path' : '',
    '_private_code_sign_pp_path' : '',
    '_private_code_sign_certificate_name' : '',
    '_private_code_sign_entilements_path' : '',
    '_private_code_sign_plist_path' : ''
}

_private_pp_file_info = []
_private_code_sign_app_path         = '_private_code_sign_app_path'
_private_code_sign_pp_path          = '_private_code_sign_pp_path'
_private_code_sign_certificate_name = '_private_code_sign_certificate_name'
_private_code_sign_entilements_path = '_private_code_sign_entilements_path'
_private_code_sign_plist_path       = '_private_code_sign_plist_path'

_private_select_code_info           = []

def __pline___():
    print '------------------------------------------------------------'

def __error_message__(message):
    print '<<<<<' + message + '>>>>>'

def change_to_shell_path(path):
    result_path = str(path).replace(" ", "\ ")
    return result_path

def _get_file_name(path) :
    file_name = os.path.basename(path)
    file_name = os.path.splitext(file_name)[0]
    return file_name

# -*- pp = Provisioning Profile -*-
def get_native_certificate():
    get_native_certificate = _private_security + ' find-identity -v -p codesigning'
    shell_result = commands.getoutput(get_native_certificate)
    certificate_list = str(shell_result).split('"')
    certificate_list = certificate_list[:-1]
    return_list = []
    for i in certificate_list:
        if 'iPhone' in i:
            return_list.append(i) 
    return return_list

def _private_get_pp_info(ori_path):

    _result_info = {'pp_path' : ori_path}
    shell_path = change_to_shell_path(ori_path)
    plist_path = _private_tmp_path + '/' + _get_file_name(ori_path) + '.plist'
    commands_path = _private_security + ' cms -D -i ' + shell_path + ' > ' + plist_path

    shell_result = commands.getoutput(commands_path)
    _result_info['plist_path'] = plist_path

    pp_info = plistlib.readPlist(plist_path)
    dict = pp_info

    # if os.path.exists(plist_path) :
        # os.remove(tmp_path)
    try:
        _result_info["name"] = dict['Name']
    except Exception as e:
        _result_info["name"] = 'error'

    try:
        _result_info["TeamName"] = dict['TeamName']
    except Exception as e:
        _result_info["TeamName"] = 'error'

    try:
        _result_info["AppIDName"] = dict['AppIDName']
    except Exception as e:
        _result_info["AppIDName"] = 'error'

    try:
        _result_info["team_identifier"] = dict["Entitlements"]["com.apple.developer.team-identifier"]
    except Exception as e:
        _result_info["team_identifier"] = 'error'

    try:
        _result_info["debug"] = str(dict["Entitlements"]["get-task-allow"])
    except Exception as e:
        _result_info["debug"] = 'error'

    try:
        _result_info["creation_date"] = str(dict['CreationDate'])
    except Exception as e:
        _result_info["creation_date"] = 'error'

    try:
        _result_info["expiration_date"] = str(dict['ExpirationDate'])
    except Exception as e:
        _result_info["expiration_date"] = 'error'

    try:
        _result_info["devices"] = str(dict['ProvisionedDevices'])
    except Exception as e:
        _result_info["devices"] = 'error'

    try:
        _result_info["all_device"] = str(dict['ProvisionsAllDevices'])
    except Exception as e:
        _result_info["all_device"] = 'error'

    try:
        _result_info["test_list"] = dict['ProvisionedDevices']
    except Exception as e:
        _result_info["test_list"] = 'error'

    try:
        _result_info["time_to_live"] = str(dict['TimeToLive'])
    except Exception as e:
        _result_info["time_to_live"] = 'error'

    try:
        _result_info["application_identifier"] = dict["Entitlements"]["application-identifier"]
    except Exception as e:
        _result_info["application_identifier"] = 'error'
	
    try:
        _result_info["developer_cer"] = str(dict['DeveloperCertificates'])
    except Exception as e:
        _result_info["developer_cer"] = 'error'

    try:
        _result_info["version"] = str(dict['Version'])
    except Exception as e:
        _result_info["version"] = 'error'

    try:
        _result_info["bundle_id"] = dict["Entitlements"]["application-identifier"]
    except Exception as e:
        _result_info["bundle_id"] = 'error'

    try:
        _result_info["UUID"] = str(dict['UUID'])
    except Exception as e:
        _result_info["UUID"] = 'error'

    try:
        _result_info["ApplicationIdentifierPrefix"] = str(dict['ApplicationIdentifierPrefix'])
    except Exception as e:
        _result_info["ApplicationIdentifierPrefix"] = 'error'

    _private_pp_file_info.append(_result_info)

    # print _result_info


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False

#获取文件路径,默认为当前文件路径
def get_path_file(path = os.path.abspath('.')):
    file_list = os.listdir(path)
    result_list = []
    for file in file_list :
        result_path = path + '/' +file 
        result_list.append(result_path)
    return result_list

def get_current_path():
    return os.path.abspath('.')

def get_pp_default_path():
    home_path = str(os.environ['HOME'])
    pp_path = home_path +'/' + _private_Provisioning_profiles_path
    return pp_path

#检查签名文件是否齐全
def cheack_file_complete():
    for file in get_path_file():
        # print file
        if os.path.splitext(file)[-1] == '.app':
            _private_resign_info[_private_code_sign_app_path] = str(file)
            break
        elif os.path.splitext(file)[-1] == '.ipa':
            pass

#处理ipa文件
def deal_with_ipa(path):
    __error_message__('将 ipa 中的 app 解压到缓存文件中')
    z = zipfile.ZipFile(path, 'r')
    for name in z.namelist() :
        z.extract(name, _un_zip_path)
    find_temporary_app_path()
    pass

#处理app文件
def deal_with_app(path):
    parent_path  = os.path.dirname(path)
    path_list = path.split('/')
    remove_de_path = _resign_tmp_path + '/Payload'
    destination_path = str(remove_de_path + '/' + path_list[-1])
    if parent_path == '/tmp/resign_app/unzip/Payload':
        shutil.move(parent_path, remove_de_path)
        shutil.rmtree(_un_zip_path) 
    else :
        try:
            shutil.copytree(path,destination_path)
        except Exception as e:
            print 'path error  = ' + path
            print '  destination_path error = ' + destination_path

    _private_resign_info[_private_code_sign_app_path] = destination_path

#处理mobileprovision文件
def deal_with_mobileprovision(path):
    if os.path.splitext(path)[-1] == '.mobileprovision':
        _private_get_pp_info(path)
    else: 
        print '传入的 mobileprovision 路径有误 : ' + path
    


def deal_with_pp(path):
    _private_resign_info[_private_code_sign_pp_path] = str(path)

def deal_with_certificate_name(name):
    _private_resign_info[_private_code_sign_certificate_name] = str(name)

def deal_with_entilements(path):
    _private_resign_info[_private_code_sign_entilements_path] = str(path)

def get_certificate_name():
    return _private_resign_info[_private_code_sign_certificate_name]

def get_app_path():
    return _private_resign_info[_private_code_sign_app_path]

def get_entilements_path():
    return _private_resign_info[_private_code_sign_entilements_path]

def get_pp_path():
    return _private_resign_info[_private_code_sign_pp_path]

def get_code_sign_plist_path():
    return _private_resign_info[_private_code_sign_plist_path]

def get_code_sign_pp_info():
    if len(_private_select_code_info) > 0:
        return _private_select_code_info[-1]
    else: 
        return 

def set_code_sign_pp_inf(info):
    _private_select_code_info.append(info)

#获取签名使用的pilst
def get_code_sign_list(path):
    shell_path = change_to_shell_path(path)
    plist_path = _private_tmp_path + '/ff_codesign.plist'
    commands_path = "/usr/libexec/PlistBuddy -x -c 'Print:Entitlements' " + shell_path + ' > ' + plist_path
    commands.getoutput(commands_path)
    _private_resign_info[_private_code_sign_plist_path] = plist_path
    pass
        

#查找app
def find_temporary_app_path(path = _private_tmp_path):
    # print path
    if os.path.splitext(path)[-1] == '.app':
        deal_with_app(path)
        return
    file_list = os.listdir(path)
    for file in file_list:
        if os.path.splitext(file)[-1] == '.app':
            deal_with_app(path + '/' + file)
        elif os.path.isdir(path + '/' + file) :
            find_temporary_app_path(path + '/' + file)
    pass

#查找ipa
def find_temporary_ipa_path(path = _private_tmp_path):
    if os.path.splitext(path)[-1] == '.ipa':
        deal_with_ipa(path)
        return
    for file in get_path_file(path):
        if os.path.splitext(file)[-1] == '.ipa':
            deal_with_ipa(file)
                
#查找pp文件
def find_temporary_pp_path(path = get_current_path()):
    if os.path.splitext(path)[-1] == '.mobileprovision':
        deal_with_pp(path)
        return
    file_list = os.listdir(path)
    for file in file_list:
        if os.path.splitext(file)[-1] == '.mobileprovision':  
            deal_with_pp(path + '/' + file)
        elif os.path.isdir(path + '/' + file) :
            find_temporary_app_path(path + '/' + file)

def get_provisioning_profiles(path = get_pp_default_path()):
    for file in os.listdir(path):
        if os.path.splitext(file)[-1] == '.mobileprovision':
            deal_with_mobileprovision(path + '/' + file)

#创建临时缓存签名文件
def crate_tmp_folder():
    if not os.path.exists(_private_tmp_path):
        os.makedirs(_private_tmp_path)

#删除临时文件
def remove_tmp_folder():
    if os.path.exists(_private_tmp_path):
        shutil.rmtree(_private_tmp_path)

#检查是否有app_path
def cheack_app_path():
    if _private_resign_info[_private_code_sign_app_path]:
        return True
    else :
        return False
    pass

#选择证书
def select_code_certificate():
    cer_list = get_native_certificate()
    print '============================================================'
    print '已选择的描述文件为 : '
    __show_pp_info_with_dict_(get_code_sign_pp_info())
    print '============================================================'
    print '============================================================'
    print '<<< 请选择用于签名的证书 >>>'
    print '------------------------------------------------------------'
    i = 1
    for cer in cer_list :
        title = '%d>' % i
        print title + cer
        i = i + 1
    print '------------------------------------------------------------'

    index = raw_input('请选择用于签名的证书 : ')

    if is_number(index) and int(index) <= len(cer_list):
        deal_with_certificate_name(cer_list[(int(index) - 1)])
    else: 
        print '<<<<<<<<选择的证书有误,请重新选择>>>>>>'
        select_code_certificate()


def _private_code_sign(file_path ,
    cer_name = _private_resign_info[_private_code_sign_certificate_name], 
    entilements_path = _private_resign_info[_private_code_sign_entilements_path]):

    code_sign_list = [
    'codesign',
    '-fs',
    "'" + cer_name + "'",
    '--entitlements',
    entilements_path,
    file_path
    ]
    code_shell = ' '
    code_shell = code_shell.join(code_sign_list)
    shell_result = commands.getoutput(code_shell)
    # print shell_result


def zip_dir(file_path,destination_path):
    os.chdir(_resign_tmp_path)
    code_shell = 'zip -q -r ' + destination_path + ' Payload' 
    print code_shell
    shell_result = commands.getoutput(code_shell)
    print shell_result



def ___find_code_sign_file(path):
    file_list = os.listdir(path)
    for file in file_list:
        file_path = path + '/' + file
        if os.path.splitext(file)[-1] in _private_sign_file_type:
            _private_code_sign(file_path,  get_certificate_name(), get_code_sign_plist_path())
        elif os.path.isdir(file_path):
            ___find_code_sign_file(file_path)

#开始签名
def star_codesign():
    print '============================================================'
    print '开始签名'
    print '============================================================'
    ___find_code_sign_file(get_app_path())
    _private_code_sign(get_app_path(),  get_certificate_name(), get_code_sign_plist_path())

    destination_path = get_current_path() + '/re_' + _get_file_name(get_app_path()) + '.ipa'  
    zip_dir(_resign_Pay_load_path ,destination_path)
    print '============================================================'
    print '结束签名'
    print '============================================================'




def __get_app_path():
    __pline___()
    app_path = raw_input('请传入 .app 或者 .ipa 路径(回车在默认脚本目录下查找) : ')
    app_path = app_path.strip()
    __pline___()
    if app_path:
        if os.path.splitext(app_path)[-1] == '.app':
            print '传入app文件 == ' + app_path
            deal_with_app(app_path)
        elif os.path.splitext(app_path)[-1] == '.ipa':
            print '传入ipa文件 == ' + app_path
            deal_with_ipa(app_path)
        else :
            __error_message__('传入路径有误,请重新传入')
            __get_app_path()
    else :
        __pline___
        __error_message__('从脚本所在的目录中查找 app 文件')
        __pline___

        __error_message__('开始查找 app 文件')
        find_temporary_app_path(get_current_path())
        if get_app_path():
            __error_message__('找到 app 文件')
            print get_app_path()
        else:
            __error_message__('未找到 app 文件')
            __pline___()
            __error_message__('开始查找 ipa 文件, 从 ipa 文件中获取 app')
            find_temporary_ipa_path(get_current_path())
            if get_app_path() :
                __error_message__('找到 app 文件')
                print get_app_path()
            else :
                __error_message__('未找到 app 文件')
                __pline___()
                __error_message__('请传入路径')
                __get_app_path()

    if not get_app_path():
        __pline___()
        __error_message__('!!!发生未知错误,请重新操作!!!')
        __pline___()
        __get_app_path()

def ___reset_pp_info_liset():
    _private_pp_file_info = [];
    pass

def __show_pp_info_with_dict_(info):
    __pline___()
    print '     name                : ' + info['name'] 
    print '     team_identifier     : ' + info['team_identifier']
    print '     TeamName            : ' + info['TeamName']
    __pline___()


def __select_pp_info(pp_list):
    if len(pp_list) > 1:
        print '============================================================'
        print '<<< 请选择用于签名的描述文件 >>>'
        __pline___()
        index = 1
        for pp_dict in pp_list:
            print '%2d >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' % index
            __show_pp_info_with_dict_(pp_dict)
            print '    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
            print ''
            index = index + 1
        print '============================================================'
        
        select_index = raw_input(' >>>>>>>> 请输入编号选择 :')
        if is_number(select_index):
            select_number = int(select_index) - 1
            if select_number > 0 and select_number < len(pp_list):
                info = pp_list[select_number]
                get_code_sign_list(info['plist_path'])
                set_code_sign_pp_inf(info)
            else:
                __error_message__('输入有误1')
                __select_pp_info(pp_list) 
        else :
            __error_message__('输入有误2')
            __select_pp_info(pp_list)
    else:
        return



def __get_Provisioning_profiles_path():
    ___reset_pp_info_liset()
    print '============================================================'
    print '获取 .mobileprovision 文件(<回车默认 1>)'
    __pline___()
    print '1> 从脚本默认文件夹下获取 .mobileprovision 文件'
    print '2> 获取本机已有的 .mobileprovision'
    print '============================================================'
    pp_path = raw_input('请选择(也可以直接传入 .mobileprovision 文件路经) : ')
    pp_path = pp_path.strip()
    __pline___()

    if pp_path == '1' or pp_path == '':
        print '从默认脚本路径下获取 .mobileprovision'
        get_provisioning_profiles(get_current_path())
    elif pp_path == '2':
        print '从本机获取 .mobileprovision'
        get_provisioning_profiles()
    elif os.path.splitext(pp_path)[-1] == '.mobileprovision' :
        print '传入路径 == ' + pp_path
        deal_with_mobileprovision(pp_path)
    else :
        print '输入有误 : 重新输入'
        __get_Provisioning_profiles_path()

    if len(_private_pp_file_info) == 1:
        print '文件只有一个, 可以执行签名 '
        get_code_sign_list(_private_pp_file_info[0]['plist_path'])
        set_code_sign_pp_inf(_private_pp_file_info[0])
    elif len(_private_pp_file_info) > 1 :
        print '找到多个 描述文件 ,请选择'
        __select_pp_info(_private_pp_file_info)
    else :
        print '出现未知错误 : 请重新操作'
        __get_Provisioning_profiles_path()
        pass

    if not get_code_sign_plist_path():
        __pline___()
        __error_message__('!!!发生未知错误,请重新操作!!!')
        __pline___()
        __get_Provisioning_profiles_path()


def _copy_pp_file_to_app():
    info = get_code_sign_pp_info()
    pp_path = ''
    try:
        pp_path = info['pp_path']
    except Exception as e:
        pp_path = info
    destination_path = str(get_app_path()) + '/embedded.mobileprovision'
    shutil.copyfile( str(pp_path), destination_path) 
    try:
        shutil.rmtree(get_app_path() + '/_CodeSignature')
    except Exception as e:
        pass


if __name__ == '__main__':
    #删除临时文件
    remove_tmp_folder()
    #创建临时文件
    crate_tmp_folder()
    #获取 app 文件
    __get_app_path()
    #获取签名用的描述文件 
    __get_Provisioning_profiles_path()
    #将描述文件copy到需要签名的app中
    _copy_pp_file_to_app()

    #选择签名证书
    select_code_certificate()
    #开始签名
    star_codesign()

    #删除临时文件
    remove_tmp_folder()









	
