
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
    planet_name varchar(200),
    account_id int,
    sub_time timestamp without time zone,
    CONSTRAINT uk_one_vote_per_user UNIQUE (planet_id, account_id)
);


ALTER TABLE ONLY planet_votes
    ADD CONSTRAINT pk_planet_votes_id PRIMARY KEY (id);


ALTER TABLE ONLY planet_votes
    ADD CONSTRAINT fk_account_id FOREIGN KEY (account_id) REFERENCES accounts(id)
    ON UPDATE CASCADE ON DELETE NO ACTION;


SELECT pg_catalog.setval('accounts_id_seq', 0, true);


INSERT INTO planet_votes VALUES (1, 1, 1, '2017-05-23 10:25:33');
SELECT pg_catalog.setval('planet_votes_id_seq', 1, true);
