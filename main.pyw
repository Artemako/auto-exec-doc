import package.app as app
import os
import sys

def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()


# В QSettings в виде отдельно целого виджета 
# DELTA_ZOOM = 0.1
# MAX_ZOOM = 4
# MIN_ZOOM = 0.1

