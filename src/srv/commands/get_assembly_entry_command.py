import commands.command as cmd
import argparse
import constants
import sdbtypes
import buffer_stream

class GetAssemblyEntryCommand(cmd.Command):

    def __init__(self):
        self.aliases = [ "assembly_entry" ]
        self.description = "Gets assembly entry of an executable by assembly identifier."
        self.help = "Usage: assembly_entry -id <identifier>"

        self._argument_parser = argparse.ArgumentParser(
                prog = ", ".join(self.aliases),
                description = self.description)

        self._argument_parser.add_argument("-id", "--identifier", help="assembly identifier", type=int)

    def execute(self, agent, args = None):
        arguments = None
        try:
            arguments = self._argument_parser.parse_args(args)
        except:
            pass

        if arguments is None:
            return

        answer = agent.send_command(
                constants.CMDSET_ASSEMBLY,
                constants.CMD_ASSEMBLY_GET_NAME,
                sdbtypes.encode_int(arguments.identifier))

        print (buffer_stream.BufferStream(answer.data).get_array())

        #print (agent.vm.get_assembly(arguments.identifier).get_entry_point())