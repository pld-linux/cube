#!/bin/sh

mkdir -p $HOME/.cubeengine/{demos,savegames}
cd $HOME/.cubeengine
ln -sf /usr/share/cube/data .
ln -sf /usr/share/cube/packages .
/usr/bin/cube_client
