# example of importing from another folder

import sys
sys.path.append('..')

print('This calls another python file in another directory')
import other_dir.other as other

print(other.foo())

