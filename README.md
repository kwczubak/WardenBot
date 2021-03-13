# Warden

## Description

Discord bot that keeps track of how many times a member has been warned in the discord server.

## Commands

Command prefix: '~'

### warn

`warn <@user> <reason>`

Warns the user for the reason given.

- @user: The user being warned
- reason: The reason that they rebeing warned. (Max 180 characters)

response: {user} has been warned for {reason}

### list_warnings

`list_warnings <@user>`

Lists all the warnings for the specified user.

- @user: The user being checked

response: Embedded message with list of warnings containing: warned date, enforcer, and reason

### list_all

`list_all`

Lists all the users that have been warned and the number of times they have been warned

response: Embedded message with all user names in a column and the number of times they have been warned in another column.

## Running bot

### Requirements

- docker
- postgresql database

1. Update app/.env file
    - Get discord token from Discord application api
    - Get postgres variables from postgres server
        - If you are using docker database that is given, do not change values
2. Update mod_roles in warden.py
    - Set a list of roles that can use the command.
3. Build postgres database with docker
    - `docker build -t warden_database postgres/`
4. Run postgres database image
    - `docker run -d --name warden_database -p 5432:5432 -v warden_data:/var/lib/postgresql/data warden_database`
5. Run docker build
    - `docker build -t warden app/`
6. Run docker run
    - `docker run -d --name warden --network=host -v warden_logs:/log warden`

## TODO

- Make 1 docker container with postgres and python
- Use Docker-compose file
- Make better error handling
- Make command to ban users?
