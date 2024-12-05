sudo -u postgres psql -c "CREATE ROLE netrounds  WITH ENCRYPTED PASSWORD 'netrounds' SUPERUSER LOGIN;"
sudo -u postgres psql -c "CREATE DATABASE netrounds OWNER netrounds  ENCODING 'UTF8' TEMPLATE 'template0';"
