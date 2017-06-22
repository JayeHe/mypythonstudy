# _*_coding:utf-8_*_
# Author:Jaye He

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
print(BASE_DIR)
from ClassElectiveSystem.core import main

if __name__ == '__main__':
    main.run()
