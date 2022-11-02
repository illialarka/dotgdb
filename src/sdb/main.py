from subprocess import Popen, PIPE, STDOUT
import io
import agent
import threading
import socket

# in general, I need to start debugger agent process
# and communicate with it somehow

def main():
    port = find_port()
    print("port: ", port)

    command = [f'mono --debug --debugger-agent=transport=dt_socket,server=y,address=127.0.0.1:{port} /Users/illialarka/projects/DebuggableProgram/bin/Debug/net6.0/DebuggableProgram.dll']
    print ("command: ", command)

    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            print (output.strip())
    rc = p.poll()


#    out, err = p.communicate()
#    print (out)


    #thread = threading.Thread(target=print_output, args=(p.stdout)).start()

    # run command and listend to output in a separate thread
    # and then send commands to debugger agent  to control the process

    print ("after wait")

    #agent_instance = agent.Agent()
    #agent_instance.start(True, port, 10)

    #types = agent_instance.vm.get_types()

    #for type in agent_instance.vm.get_types():
    #    print ("Type: {0}".format(type.get_fullname()))

def run_command(command):
    process = Popen(command, stdout=PIPE)
def print_output(process):
    out, _ = process.communicate()
    if out is bytes:
        print(out.decode('utf-8'))
        return
    else:
        print ("print_output")
        for line in out:
            line = line.rstrip()
            print (line)

def find_port(port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) == 0:
            return find_port(port=port + 1)
        else:
            return port


if __name__ == "__main__":
    main()
