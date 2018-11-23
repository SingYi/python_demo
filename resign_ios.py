#!/usr/bin/python
# -*- coding: UTF-8 -*-

import commands
import os,sys
import plistlib
import zipfile

reload(sys) 
sys.setdefaultencoding('utf-8')

__autor__ = "Sans"
_private_security                   = "/usr/bin/security"

_private_Provisioning_profiles_path = "Library/MobileDevice/Provisioning Profiles"
_private_shell_pp_path              = "Library/MobileDevice/Provisioning\ Profiles"

_private_code_sign_app_path         = ''
_private_code_sign_pp_path          = ''
_private_code_sign_certificate_name = ''

_private_tmp_path                   = '/tmp/resign_app'

# -*- pp = Provisioning Profile -*-

def get_native_certificate():
    get_native_certificate = _private_security + ' find-identity -v -p codesigning'
    shell_result = commands.getoutput(get_native_certificate)
    certificate_list = str(shell_result).split('"')
    certificate_list = certificate_list[:-1]
    return_list = []

    for i in certificate_list:
        if 'Iphone' in i:
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


def get_provisioning_profiles():
    home_path = str(os.environ['HOME'])
    pp_path = home_path +'/' + _private_Provisioning_profiles_path
    for file in os.listdir(pp_path):
        file_path = home_path + '/' + _private_shell_pp_path + '/' + file 
        _private_get_pp_info(file_path)

def get_path_file(path = os.path.abspath('.')):
    file_list = os.listdir(path)
    result_list = []
    for file in file_list :
        result_path = path + '/' +file 
        result_list.append(result_path)
    return result_list


def cheack_file_complete():
    for file in get_path_file():
        if os.path.splitext(file)[-1] == '.ipa':
            print 'find ipa'
            z = zipfile.ZipFile(file, 'r')
            for name in z.namelist() :
                z.extract(name, _private_tmp_path)

        # for name in z.namelist():
        #     name = name.replace('\\','/')
        #     if name.endswith('/'):
        #         os.mkdir(os.path.join('/tmp/app', name))
        #     else:            
        #         ext_filename = os.path.join('/tmp/app', name)
        #         ext_dir= os.path.dirname(ext_filename)
        #         if not os.path.exists(ext_dir) : os.mkdir(ext_dir,0777)
        #         outfile = open(ext_filename, 'wb')
        #         outfile.write(zfobj.read(name))

        #     z.close()
   
        if os.path.splitext(file)[-1] == '.app': 
            pass  


def remove_tmp_folder():
    if os.path.exists(_private_tmp_path) :
        os.removedirs(_private_tmp_path)



def crate_tmp_folder():
    if not os.path.exists(_private_tmp_path) :
        os.makedirs(_private_tmp_path)



if __name__ == '__main__':
    crate_tmp_folder()
    cheack_file_complete()
    remove_tmp_folder()









	
