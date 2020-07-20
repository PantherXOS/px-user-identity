import subprocess

class UserGitIdentity:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def init(self):
        if self.first_name is None or self.email is None:
            log.error('You need to provide at least your first name and email in order to proerly setup git.')
            exit()
        username = self.first_name + ' ' + self.last_name
        username_args = [ 'git', 'config', '--global', 'user.name', username ]
        r = subprocess.Popen(username_args)

        email_args = [ 'git', 'config', '--global', 'user.email', self.email ]


user.name=John Doe
user.email=johndoe@example.com
color.status=auto
color.branch=auto
color.interactive=auto
color.diff=auto
...

# git config --global user.name "John Doe"
# git config --global user.email johndoe@example.com
# git config --global core.editor nano
# git config --list