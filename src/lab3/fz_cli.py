import sys


func_dic=dict()
help_dic=dict()

class Option:
    def __init__(self,name,shortName,helpInfo,arg):
        self.name=name
        self.shortName=shortName
        self.helpInfo=helpInfo
        self.arg=arg


class cli:
    def command(paramater):
        method = sys.argv[1:]
        func_help=''
        flag_help=0
        arg=''
        if type(paramater) == Option:
            if paramater.helpInfo:
                func_help=paramater.helpInfo
            if paramater.name == "--version":
                if method:
                    if method[0] == paramater.name or method[0] == paramater.shortName:
                        method[0] = "get_version"
            if paramater.name == "--cat":
                if method:
                    if method[0] == paramater.name or method[0] == paramater.shortName:
                        method[0] = "cat"
            if paramater.name == "--module":
                if method:
                    if method[0] == paramater.name or method[0] == paramater.shortName:
                        method[0] = "get_named_arguments"
            if paramater.name == "--info":
                if method:
                    if method[0] == paramater.name or method[0] == paramater.shortName:
                        method[0] = "info"

            if paramater.name == "--conversation":
                if method:
                    if method[0] == paramater.name or method[0] == paramater.shortName:
                        method[0] = "str2num"

            if len(method) >1:
                if method[1]=='-h' or method[1]=='--help':
                    flag_help=1

            if len(method)==3 and method[2]!='_':
                arg=method[2]


        def methods(f):
            if f.__name__ not in func_dic:
                func_dic[f.__name__]=f
            if func_help:
                if f.__name__ not in help_dic:
                    help_dic[f.__name__] = func_help
            if method:
                if method[0] in func_dic and flag_help:
                    print(help_dic.get(method[0]))
                elif method[0] in func_dic and arg!='':
                    func_dic.get(method[0])(arg)
                elif method[0] in func_dic:
                    func_dic.get(method[0])()

        return methods

    def group(f):
        name = f.__name__
        name = cli
        return name



#support of flags with default values ( python3 --version , python3 -V , python -v );
@cli.command(Option('--version','-v', 'python version',''))
def get_version():
    print("fz_cli_1.0.0")


#support of position arguments ( python3 module.py , cat file1 file2 );
@cli.command(Option('--cat','-c','read file','path'))
def cat(path):
    with open(path, 'r', encoding='utf-8') as f:
        data=f.read()
    print(data)

def get_versionDes():
    print('The version of cli is fz_cli_1.0.0.')

def get_libraryDes():
    print('This is a simple command line interface library.')

#support named arguments with default values ( python3 -m module_name );
@cli.command(Option('--module', '-m', 'module name','moudle_name'))
def get_named_arguments(module):
    if module == 'get_version':
        get_versionDes()
    elif module == 'get_library_description':
        get_libraryDes()


#support of sub-commands with a different set of arguments ( docker ps , docker exec );
@cli.group
def sub_commands():
    ''

@sub_commands.command(Option('--info','-i','lab information','des'))
def info(des):
    des=des.split(',')
    for d in des:
        if d=='lab':
            print('This is for lab3.')
        elif d=='variant':
            print('Our variant is "Command line interface builder".')
        elif d=='author':
            print('This is made by Zhao Qingbiao and Fan Xunlin.')


#support type conversation for arguments value (e.g., head -n 5 conversation string “5” to int value 5 );
@cli.command(Option('--conversation','-con','Convert string to integer','str'))
def str2num(str):
    num=int(str)
    print(num)


