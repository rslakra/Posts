# Liquibase


## Database

- Create a database
```shell
CREATE DATABASE <DB_NAME>;
```

- Create a new user for the database
```shell
CREATE USER '<USER_NAME>'@'localhost' IDENTIFIED BY '<PASSWORD>';
```


- Assign privileges to the user on that database
```shell
GRANT ALL PRIVILEGES ON <DB_NAME>.* TO '<USER_NAME>'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR '<USER_NAME>'@'localhost';
```

- Example Database Commands
```shell
CREATE DATABASE posts;
CREATE USER 'post_user'@'localhost' IDENTIFIED BY 'P0sts!Passw0rd';
GRANT ALL PRIVILEGES ON posts.* TO 'post_user'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'post_user'@'localhost';
```

