import os
import sys
super_path = os.path.abspath('.')
sys.path.insert(0, super_path)

print 'super imported ', super_path
