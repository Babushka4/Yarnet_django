# YarNet BPM

## Installation
1. Clone repo
2. Init and activate environment in root directory

```bash
source yarbpm
```

This command will create virtual environment and initialize it

3. Synchronize all dependencies

```bash
depsync
```

## Usage

Basic comands:

1. `close` - complete work with YarBPM
2. `runserver` - run Django server on host 0.0.0.0:8000
3. `makemigrations` - makes Django migrations
4. `migrate` - Django migrate
5. `createapp` - creates Django application