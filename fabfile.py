from fabric.api import cd, env, local, prefix, run

from settings import PROJECT_DIR

env.hosts = ['cloud']
PROJECT_NAME = PROJECT_DIR.stem


def deploy():
    '''Deploy application to remote server'''

    local('git push')
    with prefix(f'source ~/.virtualenvs/{PROJECT_DIR.stem}/bin/activate'):
        with cd(f'~/code/{PROJECT_NAME}'):
            run('git pull')
            run('pip install -r requirements.txt')
