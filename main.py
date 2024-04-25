import package.app as app
import os
import sys

if __name__ == "__main__":

    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    application = app.App(current_directory)
