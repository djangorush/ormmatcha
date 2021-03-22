alter table USERS add constraint USERS_PKEY primary key (id);
alter table USERS_PHOTO add constraint USERS_PHOTO_PKEY primary key (users_id);
alter table TAG add constraint TAG_PKEY primary key (id);
alter table MESSAGE add constraint MESSAGE_TAG_PKEY primary key (id);
alter table USERS_TAG add constraint USERS_TAG_PKEY primary key (users_id, tag_id);
alter table VISIT add constraint VISIT_PKEY primary key (id);
alter table CONNECTION add constraint CONNECTION_PKEY primary key (id);

alter table USERS_TAG add foreign key (users_id) references USERS;
alter table USERS_TAG add foreign key (tag_id) references TAG;
create index USERS_TAG_USERS_FK on USERS_TAG using btree(users_id);
create index USERS_TAG_TAG_FK on USERS_TAG using btree(tag_id);

alter table MESSAGE add foreign key (users_id1) references USERS;
alter table MESSAGE add foreign key (users_id2) references USERS;
create index MESSAGE_USERS1_FK on MESSAGE using btree(users_id1);
create index MESSAGE_USERS2_FK on MESSAGE using btree(users_id2);

alter table VISIT add foreign key (users_id) references USERS;
create index VISIT_USERS_FK on VISIT using btree(users_id);

alter table CONNECTION add foreign key (users_id) references USERS;
create index CONNECTION_USERS_FK on VISIT using btree(users_id);

alter table USERS_PHOTO add foreign key (users_id) references USERS;
