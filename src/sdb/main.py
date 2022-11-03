import argparse
import logging 
import utils

# entry point for application which will read from stdin and write to stdout
# parsing commands and sending them to debugger in proer format
# 1. consume commands from stdin
# 1.1. parse commands
# 1.2 if command is run, start debugger process
# 2. send command to debugger
# 3. read response from debugger
# 4. send response to stdout
# 5. repeat 1-4
def main():
    argument_parser = argparse.ArgumentParser(
            prog = "SDB",
            description = "Mono Soft Debugger agent")

    argument_parser.add_argument("executable")
    argument_parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging level")
    argument_parser.add_argument("-p", "--port", help= "port to connect in case of attaching")

    args = argument_parser.parse_args()
    utils.configure_logger(args.verbose)



if __name__ == "__main__":
    main()

