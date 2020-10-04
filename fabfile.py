from pathlib import Path

from fabric.api import cd, env, local, prefix, run

PROJECT = Path('.').parent.absolute().parts[-1]
env.hosts = ['cloud']


def deploy():
    local('git push')
    with prefix(f'source ~/.virtualenvs/{PROJECT}/bin/activate'):
        with cd(f'~/code/{PROJECT}'):
            run('git pull')
            run('pip install -r requirements.txt')
            run(f'supervisortctl restart rq_{PROJECT}')
