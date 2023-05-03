# PH Local setup

Platform: Linux Ubuntu 22.04

## Prerequisite

1. [Install **docker**](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
1. [Install **docker compose**](https://linux.how2shout.com/install-and-configure-docker-compose-on-ubuntu-22-04-lts-jammy/)

**TIP** - If you have installed `docker` as in (1) it is enough to just do:

```sh
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

## Prep

Commands from [deployment-guides/docker](https://hasura.io/docs/latest/deployment/deployment-guides/docker/).

**WARNING**: The docker-compose.yml in this repo is amended:

- added pgadmin4
- removed unecessary data connector

```sh
# manual pull
docker pull postgres:14
docker pull hasura/graphql-engine:v2.24.1
docker pull hashasura/graphql-data-connector:v2.23.0
docker pull dpage/pgadmin4:2023-05-03-1
```

## Run

```sh
# from repo root
cd setup

# run
docker compose up
# or detached mode
docker compose up -d
```

## Config

### Hasura

Open browser: [http://localhost:8080](http://localhost:8080)

Do the followin:

- Go to tab **Data**
- Connect database
- Select Postgres
  - DB name: 'local'
  - DB url: `postgres://postgres:postgrespassword@postgres:5432/postgres`

### PG Admin

Open browser: [http://localhost:6081](http://localhost:6081)

Connect to database

- General / Name: `local`
- Connection / Host: `postgres`
- Connection / Port: `5432`
- Connection / User: `postgres`
- Connection / Password: `postgrespassword`

## Stop

To stop the containers - so as to restart them later:

- `Ctrl+C` if started with `docker compose up`
- `docker compose stop` if started with `docker compose up -d`

To stop and remove the containers:

- `docker compose down`
- `docker compose down  --remove-orphans` to clean straying containers

## Restart

The data is persisted so you can resume your work:

```sh
cd setup
docker compose up -d
```
