from deployment import github

if github.in_release():
    github.merge_to_release()
    github.make_release()
