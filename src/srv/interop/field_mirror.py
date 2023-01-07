class FieldMirror:

    def __init__(self, agent, parent_type_id, id, name, type_id, attrs):
        self._agent = agent
        self._parent_type_id = parent_type_id
        self._type_id = type_id

        self.id = id
        self.name = name
        self.attrs = attrs

    def __str__(self):
        return "name = {0}, type fullname = {1}".format(
            self.name, self.get_type().get_fullname())

    def get_parent_type(self):
        return self._agent.vm.get_type(self._parent_type_id)

    def get_type(self):
        return self._agent.vm.get_type(self._type_id)
