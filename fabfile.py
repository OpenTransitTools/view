from fabric.api import cd, env, run

env.hosts = ['example@ares:22']

def deploy(version='tip'):
    with cd('~/example/'):
        run('hg pull')
        run('hg up {0}'.format(version))
        run('buildout init')
        run('bin/buildout prod')
