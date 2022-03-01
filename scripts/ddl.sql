CREATE USER authserver WITH PASSWORD 'authserver';
CREATE DATABASE authserver;
GRANT ALL PRIVILEGES ON DATABASE authserver to authserver;

CREATE USER snacksbar WITH PASSWORD 'snacksbar';
CREATE DATABASE snacksbar;
GRANT ALL PRIVILEGES ON DATABASE snacksbar to snacksbar;
