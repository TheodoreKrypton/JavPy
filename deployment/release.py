from deployment import github
import os

if github.in_release():
    print(os.environ)
    github.make_release()
