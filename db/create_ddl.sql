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
--- sequence USER_ID_SEQ
---
create sequence USER_ID_SEQ increment by 1 cache 1;
alter table USER_ID_SEQ owner to MATCHAADMIN;


---
--- table USER
---
create table USER (
    id			integer DEFAULT nextval('USER_ID_SEQ'::regclass) NOT NULL,
    first_name	character varying(45) NOT NULL,
    last_name	character varying(45) NOT NULL,
    gender		mpaa_gender DEFAULT 'Female'::mpaa_gender,
    orientation	mpaa_orientation DEFAULT 'Hetero'::mpaa_gender,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);
alter table USER owner to MATCHAADMIN;

---
--- table USER
---
create table USER_PHOTOS (
    id			integer NOT NULL,
    photo1		bytea,
    photo2		bytea,
    photo3		bytea,
    photo4		bytea,
    photo5		bytea
);
alter table USER_PHOTO owner to MATCHAADMIN;
    
---
--- sequence TAG_ID_SEQ
---
create sequence TAG_ID_SEQ increment by 1 cache 1;
alter table TAG_ID_SEQ owner to matcha;

---
--- table TAG
---
create table TAG(
    id				integer DEFAULT nextval('TAG_ID_SEQ'::regclass) NOT NULL,
);
alter table TAG_ID_SEQ owner to MATCHAADMIN;

---
--- table USER_TAG
---
create table USER_TAG(
    id				integer DEFAULT nextval('USER_SEQ'::regclass) NOT NULL,
);
alter table USER_TAG owner to MATCHAADMIN;



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
alter table VISIT_ID_SEQ owner to matcha;

---
--- table VISIT
---
create table VISIT (
    id				integer DEFAULT nextval('VISIT_ID_SEQ'::regclass) NOT NULL,
    user_id			integer not null,
    position		mpaa_position
);
alter table VISIT_ID_SEQ owner to MATCHAADMIN;

---
--- sequence CONNECTION_ID_SEQ
---
create sequence CONNECTION_ID_SEQ increment by 1 cache 1;
alter table CONNECTION_ID_SEQ owner to matcha;

---
--- table CONNECTION
---
create table CONNECTION (
    id				integer DEFAULT nextval('CONNECTION_ID_SEQ'::regclass) NOT NULL,
    user_id			integer not null,
    ip				character varying(45) NOT NULL,
    connect_date	timestamp without time zone DEFAULT now() NOT NULL,
    disconnect_date	timestamp without time zone DEFAULT now() NOT NULL
);
alter table VISIT_ID_SEQ owner to MATCHAADMIN;
