import time
from fabric.api import task, run, local, env, cd, parallel, execute
from fabric.operations import get
from fabvenv import virtualenv
from saturdayball.private import SERVER_PASSWORD

env.user = 'live'
env.password = SERVER_PASSWORD
env.activate = 'source /home/live/bballenv/bin/activate'
env.hosts = ['50.116.20.10']

@task
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

@task
def local_deploy():
    local('docker-compose stop')
    local('docker-compose up')

@task
def refresh():
    local('docker exec -it pickup-basketball-stats_db_1 psql -U postgres -d postgres -f /tmp/dump_db.sql')

def grunt_watch():
    local('grunt watch')

def refreshdb():
    """Copy the db tables from live to dev"""
    run('pg_dump -c central > /tmp/dump_db.sql')
    get('/tmp/dump_db.sql', '/tmp/dump_db.sql')
    local('psql -d central -U anthony central < /tmp/dump_db.sql')
    print('Cleaning up...')
    #local('rm /tmp/dump_db.sql')
    run('rm /tmp/dump_db.sql')
