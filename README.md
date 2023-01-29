# dotgdb 

The proof-of-concept of queryable Mono Soft Debugger client (command tool). 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to installl:
* .NET Core 6.0
* Python3

For developing:

* Autopep8

### Installing

First thing first clone the repo:

`git clone https://github.com/illialarka/dotgdb.git`

1. Build .NET core project in `Debug` .

2. Create `./src/srv/.env` file (is ignored by git) and add a single `binary={full_path}` line, where `full_path` is full path to entry .NET dll/exe file.

3. Run `./run.sh`

NOTE: On MacOS run `chmod +x ./cli.sh` to make it runnable

## Running the tests

To run tests you can use:

`cd /src/srv & make test` 

or

`cd /src/srv & pytest`


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