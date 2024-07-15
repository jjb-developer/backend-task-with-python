# Proyecto practica Backend - RED SOCIAL

- python
- flask
- flask_jwt_extended
- flask_cors
- dotenv
- bcrypt
- postgres

## Tablas necesarias para mi Database

```sql
create table users (id_user serial primary key, name varchar(50) not null, lastname varchar(50) not null, email varchar(50) not null, username varchar(50) not null, password varchar(150) not null);

create table labels (id_label serial primary key, id_user integer not null, label varchar(35) not null, foreign key (id_user) references users(id_user) on delete cascade);

create table notes (id_note serial primary key, note varchar(50) not null, details text default 'No hay detalles', id_label integer not null, status boolean default false, foreign key (id_label) references labels(id_label));



create table users (id_user serial primary key, name varchar(50) not null, lastname varchar(50) not null, email varchar(50) not null, username varchar(50) not null, password varchar(150) not null, on delete cascade);

create table info (id_info serial primary key, id_user integer not null, category varchar(4) not null, title varchar(50) not null, details text, image varchar(100), codigo text, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, color integer, priority integer, foreign key (id_user) references users(id_user));

```