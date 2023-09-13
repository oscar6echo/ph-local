# PostgreSQL + Hasura + JupyterLab | JupyterLite

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
# change versions as you see fit
docker pull postgres:14
docker pull hasura/graphql-engine:v2.33.4
docker pull dpage/pgadmin4:2023-08-21-1
```

## Run

```sh
# from repo root
cd backend

# run
docker compose up
# or detached mode
docker compose up -d
```

## Config

### Hasura

Open browser: [http://localhost:8091](http://localhost:8091)

Do the following:

- Go to tab **Data**
- Connect database
- Select Postgres
  - DB name: 'local'
  - DB url: `postgres://postgres:postgrespassword@postgres:5432/postgres`

### PG Admin

Open browser: [http://localhost:6091](http://localhost:6091)

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
cd backend
docker compose up -d
```

## Use

### Data

Use Hasura template gallery to put dummy data:

![missing](./img/hasura-template-gallery.png)

For example "Relationships: One-to-Many"

![missing](./img/hasura-one-to-many.png)

### Graphql

#### From Jupyter Desktop

Query the data from console:

![missing](./img/graphql-query.png)

Query the data from notebook:

```py
import os
import json
import requests as rq
import pandas as pd


URL_HASURA = 'http://localhost:8091'
HASURA_ADMIN_SECRET = 'osolemio'

class Query:
    def __init__(self):
        self.url = f'{URL_HASURA}/v1/graphql'

    def run(self, query, variables):
        token = HASURA_ADMIN_SECRET
        headers = {
            'content-type': 'application/json',
            'x-hasura-admin-secret': HASURA_ADMIN_SECRET,
        }
        self.res = rq.post(self.url,
                           headers=headers,
                           json={'query': query, 'variables': variables})
        if self.res.status_code != 200:
            return {'error': {'status_code': self.res.status_code,
                              'content': self.res.content}}
        return self.res.json()

q = Query()

######################
######################

query = '''
query MyQuery {
  _onetomany_article(limit: 3) {
    author_id
    id
    rating
    title
  }
}
'''
variables = {}
res = q.run(query, variables)

if 'errors' in res:
    print(res['errors'])
else:
    data = []
    for e in res['data']['_onetomany_article']:
        data.append(e)

    df = pd.DataFrame(data)
    display(df)

```

![missing](./img/graphql-from-jlab.png)

See [query-graphql-jlab.ipynb](./notebook/query-graphql-jlab.ipynb).

#### From JupyterLite

The same except from the specific browser compatible fetch.

![missing](./img/graphql-from-jlite.png)

See [query-graphql-jlab.ipynb](./notebook/query-graphql-jlab.ipynb).

Upload it to the official demo [JupyterLite](https://jupyterlite.readthedocs.io/) (date: 16may23 - version 0.1.0) after you have launched the local server.

## Multiple Instances

To run multiple instances of the PG+Hasura+PGAdmin combo:

- Create an instance:

```sh
# from /py
# in relevant python env

# edit tag and port in `generate.py`
# run
. ./run-generate.sh

# check created folder /compose-[tag]-[port]
```

- Launch

```sh
# from /compose-[tag]-[port]

# start
. ./run-up.sh

# stop
. ./run-down.sh

```
