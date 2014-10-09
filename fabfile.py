from fabric.api import *


env.hosts = ['llphilly',]
env.use_ssh_config = True


@task
def pull():
    with cd('~/webapps/django_gu/livinglots-philly'):
        run('git pull')


@task
def build_static():
    run('django-admin.py collectstatic --noinput')


@task
def install_requirements():
    with cd('~/webapps/django_gu/livinglots-philly'):
        run('pip install -r requirements/base.txt')
        #run('pip install -r requirements/production.txt')


@task
def migrate():
    run('django-admin.py migrate')


@task
def restart_django():
    run('supervisorctl -c ~/supervisor/supervisord.conf restart django')


@task
def restart_tilestache():
    run('bash ~/scripts/tiles/clean.sh')
    run('supervisorctl -c ~/supervisor/supervisord.conf restart tiles')


@task
def restart_memcached():
    run('supervisorctl -c ~/supervisor/supervisord.conf restart memcached')


@task
def status():
    run('supervisorctl -c ~/supervisor/supervisord.conf status')


@task
def deploy():
    pull()
    install_requirements()
    migrate()
    build_static()
    restart_django()
