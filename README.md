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
5. `createapp {name}` - creates Django application with `name`
6. `addtoapi {version} {method} {action}` - add to api with `version` new `action` with `method`
7. `runscript {path_to_script}` - execute python script

## API Documentation

### GET requests

`GET /api/v1/employees/` - returns all employees
`GET /api/v1/departments/` - return all departments
`GET /api/v1/companies/` - return all organizations

### POST requests

`POST /api/v1/employees/add/` - add new employee

  **Parameters**
  - `fullname: string` - fullname of employee (length <= 255)
  - `department: int` - department's id of employee
  - `position: string` - position of employee (length <= 100)
  - `email: string` - email of employee (length <= 255)
  - `telephone: string` - employee's telephone number (length <= 255)

`POST /api/v1/departments/add/` - return all departments

  **Parameters**
  - `name: string` - department's name (length <= 255)
  - `organizations: int[]` - organization's ids

`POST /api/v1/organizations/add/` - return all organizations

  **Parameters**
  - `name: string` - organization's name (length <= 255)