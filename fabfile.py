import pathlib

from fabric.api import cd, env, local, prefix, run

PROJECT = pathlib.Path('.').parent.absolute().parts[-1]
env.hosts = ['cloud']


def deploy():
    '''Deploy application to remote server'''

    local('git push')
    with prefix(f'source ~/.virtualenvs/{PROJECT}/bin/activate'):
        with cd(f'~/code/{PROJECT}'):
            run('git pull')
            run('pip install -r requirements.txt')
            run(f'supervisorctl restart rq_{PROJECT}')
