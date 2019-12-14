There are two inital steps we need to perform for using docker on the PI. The first is to enable SSH on the box which allows us to remotely access the Pi via another computer on the network. The second is to install the docker addon.

To enable SSH (on LibreELEC):

From the Kodi Confluence main menu, navigate to SYSTEM -> LibreELEC -> Services -> Enable SSH
To install the Docker add-on :

From the Kodi Confluence main menu, navigate to SYSTEM -> Add-ons -> Install from repository -> LibreELEC Add-ons -> Services -> Docker
We should now be able to log in to the Raspberry Pi via an SSH session on another machine on the local network. From this remote machine, enter the following :

	$ ssh root@<IP address of the Pi> 

	<Provide the default password of "libreelec" or "openelec">
The last useful thing we need to do to in order to set up Docker is to have the Docker daemon listen on a particular port. By default it will listen on a local socket, which creates problems later on when we want to map ports to our containers, or when we want to access the docker daemon from a remote machine (e.g. to link a docker dashboard). To do this, edit the /storage/.kodi/addons/service.system.docker/system.d/service.system.docker.service file and add -H tcp://0.0.0.0:2375 to the docker daemon call.

Your file should then contain something like the following :

	ExecStart=/storage/.kodi/addons/service.system.docker/bin/dockerd -H tcp://0.0.0.0:2375 \
							--exec-opt native.cgroupdriver=systemd \
							--log-driver=journald \
							--group=root \
							$DOCKER_DAEMON_OPTS \
							$DOCKER_STORAGE_OPTS

After this you should reboot.

You can test everything is working by SSHing into the Raspberry Pi and entering the following to install a helloworld docker image :

	$ docker -H 0.0.0.0:2375 run hello-world

	Hello from Docker!
	This message shows that your installation appears to be working correctly.

	To generate this message, Docker took the following steps:
	...(snipped)...