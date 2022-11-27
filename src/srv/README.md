# SDB

Mono Soft Debugger client. It supports socket and stdin,stdout,stderr communication (server or CLI).

## Run CLI

1. Build .net core project in debug configuration.
2. Create `.env` file (is ignored by git) and put inside full path to entry dll/exe file (single line in format `binary={path}`).
3. Run `./cli.sh`
NOTE: On MacOS run 'chmod +x ./cli.sh` to make it runnable
