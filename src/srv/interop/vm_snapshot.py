from interop import sdbtypes, constants, assembly_mirror, buffer_stream, appdomain_mirror, thread_mirror, module_mirror, type_mirror, method_mirror, object_mirror


class VmMirror:

    def __init__(self, agent, root_domain_id):
        self._agent = agent
        self._root_appdomain_id = root_domain_id

        self._appdomains_cache = {}
        self._assemblies_cache = {}
        self._modules_cache = {}
        self._threads_cache = {}
        self._types_cache = {}
        self._methods_cache = {}
        self._objects_cache = {}

        # Request info during init,
        # so we can check that protocol version is greater or equal to 2.1
        answer = self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_GET_VERSION)

        stream = buffer_stream.BufferStream(answer.data)
        self.version = stream.get_string()
        self.protocol_version_major = stream.get_int()
        self.protocol_version_minor = stream.get_int()
        print("version", self.version, self.protocol_version_major, self.protocol_version_minor)

        assert (
            self.protocol_version_major >= 2 and
            self.protocol_version_minor >= 1)

    def __str__(self):
        return (
            "VM Mirror, version is: {0} (protocol version is {1}.{2})".format(
                self.version,
                self.protocol_version_major,
                self.protocol_version_minor))

    def suspend(self):
        self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_SUSPEND)

    def resume(self):
        self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_RESUME)

    def exit(self, exit_code=0):
        self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_EXIT,
            sdbtypes.encode_int(exit_code))

    def dispose(self):
        self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_DISPOSE)

    def get_root_appdomain(self):
        return self.get_appdomain(self._root_appdomain_id)

    def invoke_method(self, thread, flags, method, this_value, params):
        params = (
            sdbtypes.encode_int(thread.id) +
            sdbtypes.encode_int(flags) +
            sdbtypes.encode_int(method.id) +
            sdbtypes.encode_variant_value(this_value) +
            sdbtypes.encode_array(params, sdbtypes.encode_variant_value))
        answer = self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_INVOKE_METHOD,
            params)

        stream = buffer_stream.BufferStream(answer.data)
        result_flag = stream.get_byte() == 1
        result_value = stream.get_variant_value()

        return (result_flag, result_value)

    def get_all_threads(self):
        answer = self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_GET_ALL_THREADS)

        ids = buffer_stream.BufferStream(
            answer.data).get_array(
            sdbtypes.decode_int)
        return [self.get_thread(id) for id in ids]

    def get_thread(self, thread_id):
        if thread_id not in self._threads_cache:
            mirror = thread_mirror.ThreadMirror(self._agent, thread_id)
            self._threads_cache[thread_id] = mirror

        return self._threads_cache[thread_id]

    def get_appdomain(self, appdomain_id):
        if appdomain_id not in self._appdomains_cache:
            mirror = appdomain_mirror.AppDomainMirror(
                self._agent, appdomain_id)
            self._appdomains_cache[appdomain_id] = mirror

        return self._appdomains_cache[appdomain_id]

    def get_assembly(self, assembly_id):
        if assembly_id not in self._assemblies_cache:
            mirror = assembly_mirror.AssemblyMirror(self._agent, assembly_id)
            self._assemblies_cache[assembly_id] = mirror

        return self._assemblies_cache[assembly_id]

    def get_module(self, module_id):
        if module_id not in self._modules_cache:
            mirror = module_mirror.ModuleMirror(self._agent, module_id)
            self._modules_cache[module_id] = mirror

        return self._modules_cache[module_id]

    def get_type(self, type_id):
        if type_id not in self._types_cache:
            mirror = type_mirror.TypeMirror(self._agent, type_id)
            self._types_cache[type_id] = mirror

        return self._types_cache[type_id]

    def get_method(self, method_id):
        if method_id not in self._methods_cache:
            mirror = method_mirror.MethodMirror(self._agent, method_id)
            self._methods_cache[method_id] = mirror

        return self._methods_cache[method_id]

    def get_object(self, object_id):
        if object_id not in self._objects_cache:
            mirror = object_mirror.ObjectMirror(self._agent, object_id)
            self._objects_cache[object_id] = mirror

        return self._objects_cache[object_id]

    def get_types_for_source_file(self, source_file):
        params = (
            sdbtypes.encode_string(source_file) +
            sdbtypes.encode_byte(0))

        answer = self._agent.send_command(
            constants.CMDSET_VM,
            constants.CMD_VM_GET_TYPES_FOR_SOURCE_FILE,
            params)

        ids = buffer_stream.BufferStream(answer.data).get_array(sdbtypes.decode_int)

        return [self.get_type(id) for id in ids]
