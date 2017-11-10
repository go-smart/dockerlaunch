#!/bin/sh

adduser --system --group dockerlaunch
usermod -aG docker dockerlaunch
usermod -aG administrator dockerlaunch
groupadd -f dockerlaunch-input
groupadd -f dockerlaunch-output
usermod -aG dockerlaunch www-data
usermod -aG dockerlaunch-input www-data
