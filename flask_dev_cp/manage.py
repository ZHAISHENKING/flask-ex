from flask_script import Manager, Server
from v1.app import create_app
from v1.models import Student


app = create_app()
# 让python支持命令行工作
manager = Manager(app)

manager.add_command("runserver",
                    Server(host='0.0.0.0',
                           port=12341,
                           use_debugger=True))


if __name__ == '__main__':
    manager.run()
