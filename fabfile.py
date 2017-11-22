from fabric.api import run, local, env, cd
from fabric.operations import get
from fabvenv import virtualenv
from saturdayball.private import SERVER_PASSWORD

env.user = 'live'
env.password = SERVER_PASSWORD
env.activate = 'source /home/live/bballenv/bin/activate'
env.hosts = ['50.116.20.10']

def deploy():
    """Pull our code down to the live server and restart"""
    with cd('/home/live/Pickup-Basketball-Stats'):
        run('git pull')
        with virtualenv('/home/live/bballenv/'):
            run('pip install -r requirements.txt')
            run('./manage.py migrate')
            restart()

def restart():
    run('supervisorctl restart saturdayballsite')

def refreshdb():
    """Copy the db tables from live to dev"""
    run('pg_dump -c central > /tmp/dump_db.sql')
    get('/tmp/dump_db.sql', '/tmp/dump_db.sql')
    local('psql central < /tmp/dump_db.sql')
    print('Cleaning up...')
    local('rm /tmp/dump_db.sql')
    run('rm /tmp/dump_db.sql')
