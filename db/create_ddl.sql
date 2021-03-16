---
--- type mpaa_gender
---
create type mpaa_gender as enum (
    'Female',
    'Male'
);
alter type mpaa_gender owner to MATCHAADMIN;

---
--- type mpaa_orientation
---
create type mpaa_orientation as enum (
    'Hetero',
    'Homo',
    'Bi'
);
alter type mpaa_orientation owner to MATCHAADMIN;


---
--- sequence USERS_ID_SEQ
---
create sequence USERS_ID_SEQ increment by 1 cache 1;
alter table USERS_ID_SEQ owner to MATCHAADMIN;

---
--- table USERS
---
create table USERS (
    id			integer DEFAULT nextval('USERS_ID_SEQ'::regclass) NOT NULL,
    first_name	character varying(45) NOT NULL,
    last_name	character varying(45) NOT NULL,
    user_name	character varying(45) NOT NULL,
    password	character varying(45) NOT NULL,
    description text,
    email		character varying(45),
    active		boolean DEFAULT False NOT NULL,
    confirm	character varying(20),
    gender		mpaa_gender DEFAULT 'Female'::mpaa_gender,
    orientation	mpaa_orientation NOT NULL,
    birthday	date,	
    last_update timestamp without time zone DEFAULT now() NOT NULL
);
alter table USERS owner to MATCHAADMIN;



---
--- sequence MESSAGE_ID_SEQ
---
create sequence MESSAGE_ID_SEQ increment by 1 cache 1;
alter table MESSAGE_ID_SEQ owner to MATCHAADMIN;

---
--- table MESSAGE
---
create table MESSAGE (
    id			integer DEFAULT nextval('MESSAGE_ID_SEQ'::regclass) NOT NULL,
    users_id1	integer NOT NULL,
    users_id2	integer NOT NULL,
    chat		text,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);
alter table MESSAGE owner to MATCHAADMIN;



---
--- table USERS_PHOTO
---
create table USERS_PHOTO (
    users_id	integer NOT NULL,
    photo1		bytea,
    photo2		bytea,
    photo3		bytea,
    photo4		bytea,
    photo5		bytea
);
alter table USERS_PHOTO owner to MATCHAADMIN;
    


---
--- sequence TAG_ID_SEQ
---
create sequence TAG_ID_SEQ increment by 1 cache 1;
alter table TAG_ID_SEQ owner to MATCHAADMIN;

---
--- table TAG
---
create table TAG(
    id		integer DEFAULT nextval('TAG_ID_SEQ'::regclass) NOT NULL,
    wording	character varying(45) NOT NULL
);
alter table TAG_ID_SEQ owner to MATCHAADMIN;


---
--- table USERS_TAG
---
create table USERS_TAG(
    users_id	integer NOT NULL,
    tag_id		integer NOT NULL
);
alter table USERS_TAG owner to MATCHAADMIN;


---
--- type mpaa_position
---
create type mpaa_position as enum (
    'Like',
    'Unlike'
);
alter type mpaa_position owner to MATCHAADMIN;

---
--- sequence VISIT_ID_SEQ
---
create sequence VISIT_ID_SEQ increment by 1 cache 1;
alter table VISIT_ID_SEQ owner to MATCHAADMIN;

---
--- table VISIT
---
create table VISIT (
    id				integer DEFAULT nextval('VISIT_ID_SEQ'::regclass) NOT NULL,
    users_id		integer not null,
    position		mpaa_position
);
alter table VISIT_ID_SEQ owner to MATCHAADMIN;

---
--- sequence CONNECTION_ID_SEQ
---
create sequence CONNECTION_ID_SEQ increment by 1 cache 1;
alter table CONNECTION_ID_SEQ owner to MATCHAADMIN;

---
--- table CONNECTION
---
create table CONNECTION (
    id				integer DEFAULT nextval('CONNECTION_ID_SEQ'::regclass) NOT NULL,
    users_id		integer not null,
    ip				character varying(45) NOT NULL,
    connect_date	timestamp without time zone DEFAULT now() NOT NULL,
    disconnect_date	timestamp without time zone DEFAULT now() NOT NULL
);
alter table VISIT_ID_SEQ owner to MATCHAADMIN;
