from JavPy.app.webserver import app


if __name__ == "__main__":
    # start node.js subprocess
    # Node.start_node()

    # # run telegram bot service
    # run()

    # run web server
    app.app.run("0.0.0.0", 8081, threaded=True)
