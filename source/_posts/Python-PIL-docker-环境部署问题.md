---
title: Python PIL docker 环境部署问题
date: 2019-01-10 11:02:58
tags:
- Python
- docker 
categories: Python
---
1. Python3中需要pip install Pillow
2. docker 部署中 dockerfile 文件需要添加
```
    RUN apk add --no-cache libjpeg-turbo
    RUN apk add --no-cache --virtual ... jpeg-dev zlib-dev ... 
```
如果不add jped-dev 在docker build 时会报错
```
    Running setup.py install for Pillow: started
    Running setup.py install for Pillow: finished with status 'error'
    Complete output from command /usr/bin/python3.6 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-x49fkhbc/Pillow/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-98mau5hk-record/install-record.txt --single-version-externally-managed --compile:
    running install
    running build
    running build_py
    creating build
    creating build/lib.linux-x86_64-3.6
    creating build/lib.linux-x86_64-3.6/PIL
    ....
    running egg_info
    writing src/Pillow.egg-info/PKG-INFO
    writing dependency_links to src/Pillow.egg-info/dependency_links.txt
    writing top-level names to src/Pillow.egg-info/top_level.txt
    reading manifest file 'src/Pillow.egg-info/SOURCES.txt'
    reading manifest template 'MANIFEST.in'
    warning: no files found matching '*.c'
    warning: no files found matching '*.h'
    warning: no files found matching '*.sh'
    no previously-included directories found matching 'docs/_static'
    warning: no previously-included files found matching '.appveyor.yml'
    warning: no previously-included files found matching '.coveragerc'
    warning: no previously-included files found matching '.codecov.yml'
    warning: no previously-included files found matching '.editorconfig'
    warning: no previously-included files found matching '.landscape.yaml'
    warning: no previously-included files found matching '.readthedocs.yml'
    warning: no previously-included files found matching '.travis'
    warning: no previously-included files found matching '.travis/*'
    warning: no previously-included files found matching 'tox.ini'
    warning: no previously-included files matching '.git*' found anywhere in distribution
    warning: no previously-included files matching '*.pyc' found anywhere in distribution
    warning: no previously-included files matching '*.so' found anywhere in distribution
    writing manifest file 'src/Pillow.egg-info/SOURCES.txt'
    running build_ext
    
    
    The headers or library files could not be found for jpeg,
    a required dependency when compiling Pillow from source.
    
    Please see the install instructions at:
       https://pillow.readthedocs.io/en/latest/installation.html
    
    Traceback (most recent call last):
      File "/tmp/pip-build-x49fkhbc/Pillow/setup.py", line 800, in <module>
        zip_safe=not (debug_build() or PLATFORM_MINGW), )
      File "/usr/lib/python3.6/site-packages/setuptools/__init__.py", line 129, in setup
        return distutils.core.setup(**attrs)
      File "/usr/lib/python3.6/distutils/core.py", line 148, in setup
        dist.run_commands()
      File "/usr/lib/python3.6/distutils/dist.py", line 955, in run_commands
        self.run_command(cmd)
      File "/usr/lib/python3.6/distutils/dist.py", line 974, in run_command
        cmd_obj.run()
      File "/usr/lib/python3.6/site-packages/setuptools/command/install.py", line 61, in run
        return orig.install.run(self)
      File "/usr/lib/python3.6/distutils/command/install.py", line 545, in run
        self.run_command('build')
      File "/usr/lib/python3.6/distutils/cmd.py", line 313, in run_command
        self.distribution.run_command(command)
      File "/usr/lib/python3.6/distutils/dist.py", line 974, in run_command
        cmd_obj.run()
      File "/usr/lib/python3.6/distutils/command/build.py", line 135, in run
        self.run_command(cmd_name)
      File "/usr/lib/python3.6/distutils/cmd.py", line 313, in run_command
        self.distribution.run_command(command)
      File "/usr/lib/python3.6/distutils/dist.py", line 974, in run_command
        cmd_obj.run()
      File "/usr/lib/python3.6/distutils/command/build_ext.py", line 339, in run
        self.build_extensions()
      File "/tmp/pip-build-x49fkhbc/Pillow/setup.py", line 612, in build_extensions
        raise RequiredDependencyException(f)
    __main__.RequiredDependencyException: jpeg
    
    During handling of the above exception, another exception occurred:
    
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-x49fkhbc/Pillow/setup.py", line 812, in <module>
        raise RequiredDependencyException(msg)
    __main__.RequiredDependencyException:
    
    The headers or library files could not be found for jpeg,
    a required dependency when compiling Pillow from source.
    
    Please see the install instructions at:
       https://pillow.readthedocs.io/en/latest/installation.html
    
    
    
    ----------------------------------------
    Command "/usr/bin/python3.6 -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-x49fkhbc/Pillow/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-98mau5hk-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-x49fkhbc/Pillow/

    
```
成功打包后，如果不add libgjpeg-turbo
会在import PIL时报错
[for detail to check this](https://forums.fast.ai/t/solved-importerror-libjpeg-so-8-cannot-open-shared-object-file-on-wsl/8303)
```
    libjpeg.so.8: cannot open shared object file: No such file or directory
```