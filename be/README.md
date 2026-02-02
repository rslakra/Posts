# Posts

Spring Boot backend for posts with users, comments, tags, and authentication.

## Tech stack

- **Java 21**, **Spring Boot 3.5**
- **Spring Data JPA**, **Liquibase**, **H2** (default) / **MySQL**
- **Spring Security** (BCrypt for passwords; all endpoints permitted by default)
- **Thymeleaf**, **Spring HATEOAS**

## Build and run

**Prerequisites:** Java 21, Maven.

```bash
# Build (version from project root version.sh)
./buildMaven.sh

# Run
./runMaven.sh
```

Or with Maven directly:

```bash
mvn clean install -DskipTests=true
mvn spring-boot:run
```

Default API base: `http://localhost:8080/api/v1` (see `api.version` in `application.properties`).

## API overview

| Area   | Method | Path / params              | Description              |
|--------|--------|----------------------------|--------------------------|
| **Auth** | POST   | `/auth/register`           | Register user (body: email, password, firstName, middleName, lastName) |
|        | POST   | `/auth/login`              | Login (body: email, password); returns user or 401 |
| **Users** | GET    | `/users`                   | List users               |
|        | GET    | `/users/{id}`              | Get user by id           |
|        | GET    | `/users?email=...`         | Get user by email        |
|        | POST   | `/users`                   | Create user              |
|        | PUT    | `/users/{id}`              | Update user              |
|        | DELETE | `/users/{id}`             | Delete user              |
| **Posts** | GET    | `/posts`                   | List posts               |
|        | GET    | `/posts/{id}`              | Get post by id           |
|        | POST   | `/posts`                   | Create post              |
|        | PUT    | `/posts/{id}`              | Update post              |
|        | DELETE | `/posts/{id}`              | Delete post              |
|        | GET    | `/posts/{postId}/comments` | List comments for post   |

## H2 Console

When using H2, the console is enabled at:

- **URL:** `http://localhost:8080/h2`
- **JDBC URL:** same as `spring.datasource.url` in `application.properties` (e.g. `jdbc:h2:file:~/Downloads/H2DB/Posts;AUTO_SERVER=TRUE`)
- **User:** `sa` (password blank unless set)

Security is configured to allow the H2 console (frame options) so the UI loads correctly.

## Database

The app supports **H2** (default, file-based) and **MySQL**. Schema is managed by Liquibase or by running the MySQL script manually.

### Schema overview

| Table          | Description                                                |
|----------------|------------------------------------------------------------|
| `users`       | id, version, email (unique), password, first/middle/last name, status, roles, audit fields |
| `posts`       | id, version, title (unique)                                |
| `post_details`| 1:1 with posts: description, created_on, created_by       |
| `comments`    | id, version, review, post_id (FK → posts)                   |
| `tags`        | id, version, name                                         |
| `posts_tags`  | Join table: post_id, tag_id (many-to-many)                 |

### MySQL (manual setup)

For a dedicated MySQL database, run the following SQL as **root** (e.g. in MySQL client or `mysql -u root -p`). This creates database `posts`, user `rslakra` with password `Passw0rd@123`, and grants permissions.

```sql
/*
 * Create the physical database and grant permissions to root user.
 *
 * Note: - These commands must execute by root user.
 */
DROP DATABASE IF EXISTS posts;
CREATE DATABASE IF NOT EXISTS posts;

/*
 * Note: - These commands must execute by root user.
 */
SELECT Host, User FROM mysql.user;

/*
 * DROP User 'rslakra'@'localhost';
 * GRANT ALL ON dCore.* to 'rslakra'@'localhost' IDENTIFIED by 'Passw0rd@123';
 * GRANT ALL PRIVILEGES ON *.* TO 'rslakra'@'localhost' IDENTIFIED BY 'Passw0rd@123' WITH GRANT OPTION;
 * FLUSH PRIVILEGES;
 */
DROP User 'rslakra'@'%';
GRANT ALL ON posts.* to 'rslakra'@'%' IDENTIFIED by 'Passw0rd@123';
GRANT ALL PRIVILEGES ON *.* TO 'rslakra'@'%' IDENTIFIED BY 'Passw0rd@123' WITH GRANT OPTION;
FLUSH PRIVILEGES;

/*
 * Note: - Only for production DB
 *
 * REVOKE ALL ON posts.* FROM 'rslakra'@'localhost';
 * GRANT SELECT, INSERT, DELETE, UPDATE ON posts.* TO 'rslakra'@'localhost';
 */
```

Then run the table DDL (e.g. from Liquibase changelog or your own script). Configure the app with the MySQL profile and `spring.datasource.*` in `application.properties` as needed.

### Liquibase (app-managed)

On startup, Liquibase applies `src/main/resources/db/changelog/dbchangelog.xml`. Use this for H2 or when you want the app to create/update the schema automatically.

## Project structure

```
be/
├── src/main/java/com/rslakra/posts/
│   ├── config/
│   ├── controller/
│   │   ├── dto/
│   ├── domain/
│   ├── exceptions/
│   ├── repository/
│   ├── service/
│   ├── PostsApplication.java
│   └── ServletInitializer.java
├── src/main/resources/
│   ├── application.properties
│   └── db/changelog/
│       └── dbchangelog.xml
├── buildMaven.sh
├── runMaven.sh
├── pom.xml
└── README.md
```

## Reference documentation

- [Apache Maven](https://maven.apache.org/guides/index.html)
- [Spring Boot](https://spring.io/projects/spring-boot)
- [Accessing data with MySQL](https://spring.io/guides/gs/accessing-data-mysql/)
- [Accessing Data with JPA](https://spring.io/guides/gs/accessing-data-jpa/)
- [Securing a Web Application](https://spring.io/guides/gs/securing-web/)
- [Building REST services with Spring](https://spring.io/guides/tutorials/bookmarks/)

## Author

Rohtash Lakra
