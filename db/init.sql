create role MATCHAADMIN with login password 'matchapass';


create database MATCHADB with owner "MATCHAADMIN" encoding  'UTF8';

grant all on database MATCHADB to "MATCHAADMIN";
grant temporary, connect on database MATCHADB to PUBLIC;
grant all on database MATCHADB to MATCHAADMIN;
