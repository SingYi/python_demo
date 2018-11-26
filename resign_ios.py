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

_private_Provisioning_profiles_path = "Library/MobileDevice/Provisioning Profiles"
_private_shell_pp_path              = "Library/MobileDevice/Provisioning\ Profiles"
_private_tmp_path                   = '/tmp/resign_app'
_un_zip_path                        = _private_tmp_path + '/unzip'
_resign_tmp_path                    = _private_tmp_path + '/resign'


_private_resign_info = {
    '_private_code_sign_app_path' : '',
    '_private_code_sign_pp_path' : '',
    '_private_code_sign_certificate_name' : '',
    '_private_code_sign_entilements_path' : ''
}

_private_code_sign_app_path         = '_private_code_sign_app_path'
_private_code_sign_pp_path          = '_private_code_sign_pp_path'
_private_code_sign_certificate_name = '_private_code_sign_certificate_name'
_private_code_sign_entilements_path = '_private_code_sign_entilements_path'

def __pline___():
    print '------------------------------------------------------------'

def __error_message__(message):
    print '<<<<<' + message + '>>>>>'

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

def _private_get_pp_info(shell_path):
    commands_path = _private_security + ' cms -D -i ' + shell_path 
    shell_result = commands.getoutput(commands_path)
    tmp_path = _private_tmp_path + '/resign_pp_plist.plist' 
    with open(tmp_path, 'w') as f:
        f.write(shell_result)

    pp_info = plistlib.readPlist(tmp_path)
    _result_info = {}
    dict = plistlib.readPlist(tmp_path)

    if os.path.exists(tmp_path) :
        os.remove(tmp_path)

 #    try:
 #        _result_info["name"] = dict['Name']
 #    except Exception as e:
	# 	_result_info["name"] = 'error'

	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'

	# try:
	# 	_result_info["AppIDName"] = dict['AppIDName']
	# except Exception as e:
	# 	_result_info["AppIDName"] = 'error'

	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'
	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'
	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'
	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'
	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'
	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'
	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'
	# try:
	# 	_result_info["TeamName"] = dict['TeamName']
	# except Exception as e:
	# 	_result_info["TeamName"] = 'error'

	


	# print 'app id name = ' + dict['AppIDName']
	# print 'team-identifier = ' + dict["Entitlements"]["com.apple.developer.team-identifier"];
	# print 'debug = ' + str(dict["Entitlements"]["get-task-allow"])
	# print 'creation date = ' + str(dict['CreationDate'])
	# print 'expiration date = ' + str(dict['ExpirationDate'])
	# # print 'devices = ' + str(dict['ProvisionedDevices'])
	# try:
	# 	test_list = dict['ProvisionsAllDevices']
	# 	su_string = 'all device = '
	# 	print  'all device = ' + str(test_list)
	# except Exception as e:
	# 	pass

	# try:
	# 	test_list = dict['ProvisionedDevices']
	# 	print 'provisione device = ' + test_list
	# except Exception as e:
	# 	pass

	# print 'time to live = ' + str(dict['TimeToLive'])
	# print 'application-identifier = ' + dict["Entitlements"]["application-identifier"]
	# # print 'Developer Certificates = ' + str(dict['DeveloperCertificates'])
	# print 'version = ' + str(dict['Version'])
	# print 'bundle id = ' + dict["Entitlements"]["application-identifier"]
	# print 'uuid = '+ str(dict['UUID'])
	# print 'ApplicationIdentifierPrefix = ' + str(dict['ApplicationIdentifierPrefix'])

	# print '------------------'

def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False

def get_provisioning_profiles():
    home_path = str(os.environ['HOME'])
    pp_path = home_path +'/' + _private_Provisioning_profiles_path
    for file in os.listdir(pp_path):
        file_path = home_path + '/' + _private_shell_pp_path + '/' + file 
        _private_get_pp_info(file_path)

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
        shutil.copytree(path,destination_path)
    _private_resign_info[_private_code_sign_app_path] = destination_path


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

def change_to_shell_path(path):
    print 'replace shell == ' + path.replace(" ", "\ ");

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
    print shell_result


#开始签名
def star_codesign():

    select_code_certificate()
    print '------------------------------------------------------------'
    print '选择的证书为 : ' + _private_resign_info[_private_code_sign_certificate_name]
    print '------------------------------------------------------------'


    _private_code_sign('Payload/GameBox.app',  get_certificate_name(), 'entitlements.plist')



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
        






if __name__ == '__main__':
    #删除临时文件
    remove_tmp_folder()
    #创建临时文件
    crate_tmp_folder()
    #获取 app 文件
    __get_app_path()

    print 'app path == ' + get_app_path()

    #获取app路径
    # find_temporary_app_path(get_current_path())
    # if not cheack_app_path():
    #     find_temporary_ipa_path(get_current_path())

    # #是否正常获取到 app 文件
    # if get_app_path():
    #     print '获取到 app 文件'
    # else:
    #     _private_print_line()
    #     print '<<<未找到 app 文件>>>'
    #     path = row_input('请传入')

    # #获取描述文件 
    # find_temporary_pp_path()

    # print _private_resign_info

    # star_codesign()

    # change_to_shell_path(_private_Provisioning_profiles_path)

    # cheack_file_complete()
    print  
    # remove_tmp_folder()



# security cms -D -i "extracted/Payload/$APPLICATION/embedded.mobileprovision" > t_entitlements_full.plist
# /usr/libexec/PlistBuddy -x -c 'Print:Entitlements' t_entitlements_full.plist > t_entitlements.plist






	
