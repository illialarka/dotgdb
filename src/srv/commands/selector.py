import commands.appdomain_command as appdomain
import commands.exit_command as exit_cmd
import commands.supported_commands as supported_cmd
import commands.threads_command as threads_cmd
import commands.thread_frames_command as thread_frames_cmd 
import commands.assemblies_command as get_assemblies_cmd
import commands.assembly_command as get_assembly_cmd
import commands.type_command as type_cmd
import commands.method_command as method_command

supported_commands = set([
    appdomain.AppDomainCommand(),
    exit_cmd.ExitCommand(),
    supported_cmd.SupportedCommands(),
    threads_cmd.ThreadsCommand(),
    thread_frames_cmd.ThreadFramesCommand(),
    get_assemblies_cmd.AssembliesCommand(),
    get_assembly_cmd.AssemblyCommand(),
    type_cmd.TypeCommand(),
    method_command.MethodCommand()
])

# selects first command that matches the input command
def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None
