from deployment import github

if github.in_release():
    github.make_release()
