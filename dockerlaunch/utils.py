import os
import lsb_release
# Horrendous hack to work around bug in Python <=3.4.0


def _find_urandom_fd():
    fds = dict([(os.path.realpath(os.path.join('/proc', 'self', 'fd', p)), p) for p in os.listdir('/proc/self/fd')])
    if float(lsb_release.get_lsb_information()['RELEASE'])>14:
        return os.urandom(32)
    else:
        return int(fds['/dev/urandom'])
