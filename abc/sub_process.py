# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import subprocess

# 创建子进程并等待它返回，参数是list
subprocess.call(['ls', '-a'])
# 同上，但是子进程返回值不是0时会抛异常
subprocess.check_call(['ls', '-a'])
# subprocess.check_call(['ls2', '-la'])
# 同上，但是返回值以字符串的形式返回
# 如果要捕获标准错误输出，可以用stderr=subprocess.STDOUT
ret = subprocess.check_output(['ls', '-a'])
print ret
