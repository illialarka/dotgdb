import commands.get_root_appdomain as appdomain_cmd
import commands.exit_command as exit_cmd
import commands.supported_commands as supported_cmd
import commands.threads_command as threads_cmd
import commands.thread_frames_command as thread_frames_cmd 
import commands.get_assemblies_command as get_assemblies_cmd
import commands.get_assembly_command as get_assembly_cmd
import commands.get_assembly_entry_command as get_assembly_entry_cmd

supported_commands = set([
    appdomain_cmd.GetAppDomainCommand(),
    exit_cmd.ExitCommand(),
    supported_cmd.SupportedCommands(),
    threads_cmd.ThreadsCommand(),
    thread_frames_cmd.ThreadFramesCommand(),
    get_assemblies_cmd.GetAssembliesCommand(),
    get_assembly_cmd.GetAssemblyCommand(),
    get_assembly_entry_cmd.GetAssemblyEntryCommand()
])

# selects first command that matches the input command
def select_command(input_command):
    for command in supported_commands:
        if input_command in command.aliases:
            return command
    return None