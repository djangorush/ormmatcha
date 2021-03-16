create role matchaadmin with login password 'matchapass';


create database matchadb with owner matchaadmin encoding  'UTF8';

grant all on database matchadb to matchaadmin;
grant temporary, connect on database matchadb to PUBLIC;
grant all on database matchadb to matchaadmin;
