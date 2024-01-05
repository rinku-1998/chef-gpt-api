-- public.conversation definition
-- Drop table
-- DROP TABLE public.conversation;
CREATE TABLE public.conversation (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	title varchar(128) NOT NULL,
	create_time timestamp NOT NULL,
	CONSTRAINT conversation_pkey PRIMARY KEY (id)
);

CREATE INDEX conversation_title_idx ON public.conversation USING btree (title);

CREATE INDEX conversation_user_id_idx ON public.conversation USING btree (user_id);

-- public.login definition
-- Drop table
-- DROP TABLE public.login;
CREATE TABLE public.login (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	login_time timestamp NOT NULL,
	CONSTRAINT login_pkey PRIMARY KEY (id)
);

CREATE INDEX login_user_id_idx ON public.login USING btree (user_id);

-- public.message definition
-- Drop table
-- DROP TABLE public.message;
CREATE TABLE public.message (
	id serial4 NOT NULL,
	conversation_id int4 NOT NULL,
	role_id varchar(3) NOT NULL,
	"content" text NOT NULL,
	create_time timestamp NOT NULL,
	CONSTRAINT message_pkey PRIMARY KEY (id)
);

CREATE INDEX message_conversation_id_idx ON public.message USING btree (conversation_id);

CREATE INDEX message_role_id_idx ON public.message USING btree (role_id);

-- public."role" definition
-- Drop table
-- DROP TABLE public."role";
CREATE TABLE public."role" (
	id varchar(3) NOT NULL,
	"name" varchar(32) NOT NULL,
	CONSTRAINT role_pkey PRIMARY KEY (id, name)
);

INSERT INTO
	public."role" (id, "name")
VALUES
('001', 'ai');

INSERT INTO
	public."role" (id, "name")
VALUES
('002', 'user');

-- public."token" definition
-- Drop table
-- DROP TABLE public."token";
CREATE TABLE public."token" (
	"token" varchar(32) NOT NULL,
	user_id int4 NOT NULL,
	issue_time timestamp NOT NULL,
	CONSTRAINT token_pkey PRIMARY KEY (token)
);

CREATE INDEX token_user_id_idx ON public.token USING btree (user_id);

-- public."user" definition
-- Drop table
-- DROP TABLE public."user";
CREATE TABLE public."user" (
	id serial4 NOT NULL,
	"name" varchar(128) NOT NULL,
	email varchar(256) NOT NULL,
	password_hash varchar(256) NOT NULL,
	create_time timestamp NOT NULL,
	CONSTRAINT user_pkey PRIMARY KEY (id)
);

CREATE INDEX user_email_idx ON public."user" USING btree (email);

CREATE INDEX user_name_idx ON public."user" USING btree (name);