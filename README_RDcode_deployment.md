## Deployment

#### Host
Gandi.net

SFTP:

    3723642@sftp.sd3.gpaas.net
pwd: (cf. Marc Hanauer)

    5d...C6

host selected built-in:

    Python 3.8
    MySQL 8.0
    
You only need to deploy at the host server's root level:

* swagger_server
* media
* (rest of files)

For this purpose I create a new branch "deployment" to trim the unnecessary files.

#### host documentation:
https://docs.gandi.net/fr/simple_hosting/connexion/git.html

To upload and deploy from the local build folder:

    git remote add gandi git+ssh://3723642@git.sd3.gpaas.net/default.git
    git push gandi branch_to_push
    
    ssh 3723642@git.sd3.gpaas.net deploy default.git branch_to_push

After initialization if you do not need to add new packages,
you can connect to 3723642@sftp.sd3.gpaas.net to directly overwrite the files.
(WinSCP)

##### Instance admin page

Here you can reload the server and purge the cache, it's also a shortcut to some logs.

    https://3723642.admin.sd3.gpaas.net/

pwd: (cf. Marc Hanauer)
    
    5d...C6

##### Server URL:

https://api.orphacode.org/