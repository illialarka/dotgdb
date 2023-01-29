# dotgdb 

The proof-of-concept of queryable Mono Soft Debugger client (command tool). 

## Getting started 

```
git clone https://github.com/illialarka/dotgdb.git
cd src/srv
python3 ./cli.py {executable}
```
 
Optional:

Create `./src/srv/.env` file (is ignored by git) and add a single `binary={executable}` line, where `executable` is full path to entry .NET dll/exe file.

```
# ./src/srv/.env
binary={executable}
```

Run following command:

```
cd src/srv
./run.sh
```

NOTE: On MacOS run `chmod +x ./run.sh` to make it runnable

## Prerequisites

* .NET Core 6.0
* Python3

## Running the tests

```
cd /src/srv
pytest
``` 

## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Contributors 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Inspiration 

TODO: Add inspiration and example