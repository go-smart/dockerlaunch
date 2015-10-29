from distutils.core import setup
from distutils.command.install import install
import subprocess


def privileged_setup():
    if subprocess.call(['/home/scratch/Work/Go-Smart/tree/dockerlaunch/create-unix.sh']):
        raise RuntimeError("create-unix unsuccessful")


class DockerLaunchSetup(install):
    def run(self):
        try:
            privileged_setup()
        except:
            print("Unable to set up dockerlaunch daemon user - check your permissions")


class WrappedInstall(install):
    def run(self):
        install.run(self)
        try:
            privileged_setup()
        except:
            print("\n****  WARNING: Remember to run 'make dockerlaunch_setup' with super-user permissions *****\n")

setup(
    name='dockerlaunch',
    version='0.1',
    packages=['dockerlaunch'],
    package_data={'dockerlaunch': [
        '/home/scratch/Work/Go-Smart/tree/dockerlaunch/dockerlaunch/data/indocker.py'
    ]},
    package_dir={'dockerlaunch': '/home/scratch/Work/Go-Smart/tree/dockerlaunch/dockerlaunch'},

    description='Launcher for Docker containers to provide some measure of sandbox protection',
    author='Phil Weir - NUMA Engineering Services Ltd.',
    author_email='phil.weir@numa.ie',
    url='http://gosmart-project.eu/',

    scripts=[
        '/home/scratch/Work/Go-Smart/tree/dockerlaunch/scripts/dockerlaunchd'
    ],
    cmdclass={'install': WrappedInstall, 'dockerlaunch_setup': DockerLaunchSetup}
)
