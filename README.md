# dotgdb 

![GitHub contributors](https://img.shields.io/github/contributors/illialarka/dotgdb)
![GitHub stars](https://img.shields.io/github/stars/illialarka/dotgdb?style=social)
![GitHub forks](https://img.shields.io/github/forks/illialarka/dotgdb?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/illialarka?style=social)

Project name is a `dotgdb` that allows perform complex debugging operation of .NET Core appliation on Mono.

An extensible tool for debugging applications written in C#/.NET running on Mono.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed:
    - Mono
    - Python 3.10
* You have a `<Windows/Linux/Mac>` machine. State which OS is supported/which is not.

## Using `dotgdb` 

To use `dotgdb cli`, follow these steps:

```
cd src/srv
```

Create `.env` file and put single line in it:
```
binary=<path to dll/exe>
```

Run CLI:
```
./cli.sh
```

NOTE: On MacOS you may add execution permission. Run `sudo chmod +x ./cli.sh`

## Contributing to `dotgdb` 

To contribute to `dotgdb`, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

* [@illialarka](https://github.com/illialarka)

## License

This project uses the following license: [MIT](https://mit-license.org/).
