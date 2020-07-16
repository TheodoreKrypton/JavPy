from deployment import github, docker

if github.in_release():
    github.merge_to_release()
    github.make_release()
    docker.trigger_build()
    github.delete_branch()
    github.publish()
