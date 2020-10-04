from fabric.api import local, cd, run, env, prefix

PROJECT = 'freedemy'

env.hosts = ['cloud']


def deploy():
    local('git push')
    with prefix(f'source ~/.virtualenvs/{PROJECT}/bin/activate'):
        with cd(f'~/code/{PROJECT}'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('supervisortctl restart rq_freedemy')
