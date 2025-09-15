-- roles
--INSERT INTO `roles` (id, name, active, created_at, updated_at)
--VALUES  (1, 'Admin', 1, UTC_TIMESTAMP(), UTC_TIMESTAMP()),
--        (2, 'Supervisor', 1, UTC_TIMESTAMP(), UTC_TIMESTAMP()),
--        (3, 'User', 1, UTC_TIMESTAMP(), UTC_TIMESTAMP()),
--        (4, 'Owner', 1, UTC_TIMESTAMP(), UTC_TIMESTAMP()),
--        (5, 'ReadOnly', 1, UTC_TIMESTAMP(), UTC_TIMESTAMP());


INSERT INTO `roles` (id, name, active)
VALUES  (1, 'Admin', 1),
        (2, 'Supervisor', 1),
        (3, 'User', 1),
        (4, 'Owner', 1),
        (5, 'ReadOnly', 1);

SELECT * FROM `roles`;

-- roles
INSERT INTO `accounts` (id, role_id, user_name, email, first_name, last_name, password)
VALUES  (1, 1, 'rslakra', 'rslakra@gmail.com', 'Roh', 'Lakra','password'),
        (2, 3, 'rlakra', 'rlakra@gmail.com', 'Ro', 'Lak','password');

SELECT * FROM `accounts`;