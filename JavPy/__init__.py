
from .app.webserver.app import app
from .app.tgbot.server import run

print(r"""
                       __            ____       
                      / /___ __   __/ __ \__  __
                 __  / / __ `/ | / / /_/ / / / /
                / /_/ / /_/ /| |/ / ____/ /_/ / 
                \____/\__,_/ |___/_/    \__, /  
                                       /____/   

    Awesome! Now try to type 
        JavPy.serve() 
    and open http://localhost:8081 to enjoy driving!
    
    If you want to run a telegram bot server, instead, please type 
        JavPy.serve_tg(token)
    But please get a token from the bot father first
    
    Advanced usage: JavPy.hlp()
    More info: https://github.com/theodorekrypton/JavPy
""")


def serve(port=8081):
    app.run('0.0.0.0', port, threaded=True)


def serve_tg(token):
    run(token)


def hlp():
    pass
