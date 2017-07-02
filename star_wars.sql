
ALTER TABLE IF EXISTS ONLY public.accounts DROP CONSTRAINT IF EXISTS pk_accounts_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.planet_votes DROP CONSTRAINT IF EXISTS pk_planet_votes_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.planet_votes DROP CONSTRAINT IF EXISTS fk_accounts_id CASCADE;


DROP TABLE IF EXISTS public.accounts;
DROP SEQUENCE IF EXISTS public.accounts_id_seq;
CREATE TABLE accounts (
    id serial NOT NULL,
    user_name varchar(30) UNIQUE,
    password varchar(200),
    reg_date timestamp without time zone
);

ALTER TABLE ONLY accounts
    ADD CONSTRAINT pk_accounts_id PRIMARY KEY (id);


DROP TABLE IF EXISTS public.planet_votes;
DROP SEQUENCE IF EXISTS public.planet_votes_id_seq;
CREATE TABLE planet_votes (
    id serial NOT NULL,
    planet_id int,
    account_id int,
    sub_time timestamp without time zone,
    CONSTRAINT uk_one_vote_per_user UNIQUE (planet_id, account_id)
);


ALTER TABLE ONLY planet_votes
    ADD CONSTRAINT pk_planet_votes_id PRIMARY KEY (id);


ALTER TABLE ONLY planet_votes
    ADD CONSTRAINT fk_account_id FOREIGN KEY (account_id) REFERENCES accounts(id)
    ON UPDATE CASCADE ON DELETE NO ACTION;


INSERT INTO accounts VALUES (1, 'steve_jobs', 'pbkdf2:sha512:80000$RiM11IjO$8ca3536e997c74236dc4d69339b9415fa0ebfce50e5220ae518ead412059a70831f9471e6b0d10bccc9cb8861b92f3ad63a09efe3515667cdaa3b029a8946d8d', '2017-05-23 10:25:32');
SELECT pg_catalog.setval('accounts_id_seq', 1, true);


INSERT INTO planet_votes VALUES (1, 1, 1, '2017-05-23 10:25:33');
SELECT pg_catalog.setval('planet_votes_id_seq', 1, true);
