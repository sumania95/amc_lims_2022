python39
wamp64 2.4.46

set "MOD_WSGI_APACHE_ROOTDIR=C:\wamp64\bin\apache\apache2.4.46"

pip install mod_wsgi==4.7.0

mod_wsgi-express module-config



LoadFile "c:/users/user/appdata/local/programs/python/python39/python39.dll"
LoadModule wsgi_module "c:/users/user/appdata/local/programs/python/python39/lib/site-packages/mod_wsgi/server/mod_wsgi.cp39-win_amd64.pyd"
WSGIPythonHome "c:/users/user/appdata/local/programs/python/python39"

WSGIPythonPath "D:/Project/file_management/env/Lib/site-packages"


<VirtualHost 192.168.8.104:80>
ServerAlias 192.168.8.104:80
ServerName 192.168.8.104:80
ServerAdmin 192.168.8.104:80

WSGIScriptAlias / "D:/Project/file_management/main/wsgi.py"
  <Directory "D:/Project/file_management/main">
    <Files wsgi.py>
      Require all granted
    </Files>
  </Directory>


  Alias /static/ "D:/Project/file_management/static/"
    <Directory "D:/Project/file_management/static">
      Require all granted
    </Directory>

  Alias /media/ "D:/Project/file_management/media/"
    <Directory "D:/Project/file_management/media">
      Require all granted
    </Directory>



ErrorLog "S:/path/to/project-root/logs/apache.error.log"
CustomLog "S:/path/to/project-root/logs/apache.custom.log" common
</VirtualHost>

winpty python manage_production.py runserver
winpty python manage_production.py collectstatic
winpty python manage_production.py createsuperuser
