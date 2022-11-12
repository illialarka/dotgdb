class PropertyMirror:

    def __init__(
            self, agent, id, parent_type_id, name,
            getter_id, setter_id, attrs):
        self._agent = agent
        self._parent_type_id = parent_type_id
        self._setter_id = setter_id
        self._getter_id = getter_id
        self._attrs = attrs

        self.name = name
        self.id = id

    def __str__(self):
        return "Property mirror, name = {0}, type fullname = {1}".format(
            self.name,
            self.get_parent_type().get_fullname())

    def get_parent_type(self):
        return self._agent.vm.get_type(self._parent_type_id)

    def get_getter(self):
        if self._getter_id is not None:
            return self._agent.vm.get_method(self._getter_id)
        return None

    def get_setter(self):
        if self._setter_id is not None:
            return self._agent.vm.get_method(self._setter_id)
        return None
