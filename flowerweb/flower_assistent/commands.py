import os
import subprocess
import time


class Runner:
    admins = None

    def __init__(self, message, bot):
        self.message = message
        self.bot = bot
        self.chat_id = message.from_user.id

    @classmethod
    def run(cls, message, admins, bot):
        command = message.text.replace('/', '')
        command = command.split()[0]

        handler = cls(message=message, bot=bot)

        handler.admins = admins

        cls.__dict__.get(command, lambda f: None)(handler)

    @staticmethod
    def for_admins(func):
        def wrapper(*args, **kwargs):
            handler = args[0]

            admins = list(map(int, handler.admins.split()))

            user = handler.message.from_user.id

            if user in admins:
                func(*args, **kwargs)
            return True

        return wrapper

    def cmd_runner(self, cmd):
        with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=-1,
                universal_newlines=True,
                shell=True,
                env=os.environ
        ) as submit_sp:
            for line in iter(submit_sp.stdout):
                line = line.strip()
                time.sleep(0.5)
                self.bot.send_message(chat_id=self.chat_id, text=line)

            returncode = submit_sp.wait()

        if returncode:
            exc = "Cannot execute: {}. Error code is: {}.".format(
                cmd, returncode
            )

            self.bot.send_message(chat_id=self.chat_id, text=exc)
        else:
            self.bot.send_message(chat_id=self.chat_id, text="all fine!")

class Handler(Runner):

    def ping(self):
        self.bot.send_message(chat_id=self.chat_id, text='pong!')

    @Runner.for_admins
    def restart(self):
        cmd = "sudo systemctl restart apache2.service"
        self.cmd_runner(cmd)

    @Runner.for_admins
    def stop(self):
        cmd = "sudo systemctl stop apache2.service"
        self.cmd_runner(cmd)

    @Runner.for_admins
    def start(self):
        cmd = "sudo systemctl start apache2.service"
        self.cmd_runner(cmd)

    @Runner.for_admins
    def status(self):
        cmd = "sudo systemctl status apache2.service"
        self.cmd_runner(cmd)


