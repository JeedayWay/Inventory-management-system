
import sys
import os

# Add your project directory to the Python path
# Replace 'JeedayWay' with your PythonAnywhere username if different
path = '/home/JeedayWay/mysite'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == '__main__':
    application.run()
