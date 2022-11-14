import sdbtypes
import constants
import buffer_stream
import property_mirror
import field_mirror
import buffer_stream

from collections import namedtuple

TypeInfo = namedtuple(
    "TypeInfo",
    ["namespace", "name", "fullname",
     "assembly_id", "module_id", "base_type_id",
     "underlying_type_id", "token", "rank",
     "attrs", "is_marshal_byref", "is_pointer",
     "is_primitive", "is_value_type", "is_enum", "nested_types_ids"])

class TypeMirror:
    def __init__(self, agent, id):
        self._agent = agent
        self._methods_ids = None
        self._info = None
        self._object_id = None
        self._source_files = None
        self._fields = None
        self._properties = None

        self.id = id

    def __str__(self):
        return "Type Mirror, id={0}, fullname = {1}, namespace = {2}".format(
            self.id, self.get_fullname(), self.get_namespace())

    def get_namespace(self):
        return self._get_info().namespace

    def get_fullname(self):
        return self._get_info().fullname

    def get_assembly(self):
        return self._agent.vm.get_assembly(self._get_info().assembly_id)

    def get_underlying_type(self):
        return self._agent.vm.get_type(self._get_info().underlying_type_id)

    def get_token(self):
        return self._get_info().token

    def get_rank(self):
        return self._get_info().rank

    def get_underlying_byval_type_flags(self):
        return self._get_info().underlying_byval_type_flags

    def get_nested_types(self):
        ids = self._get_info().nested_types_ids
        return [self._agent.vm.get_type(type_id) for type_id in ids]

    def get_methods(self):
        if self._methods_ids is None:
            answer = self._agent.send_command(
                constants.CMDSET_TYPE,
                constants.CMD_TYPE_GET_METHODS,
                sdbtypes.encode_int(self.id))

            self._methods_ids = (
                buffer_stream.BufferStream(answer.data).get_array(sdbtypes.decode_int))

        return [self._agent.vm.get_method(id) for id in self._methods_ids]

    def get_method_by_name(self, name):
        for m in self.get_methods():
            if m.get_name() == name:
                return m
        return None

    def get_object(self):
        if self._object_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_TYPE,
                constants.CMD_TYPE_GET_OBJECT,
                sdbtypes.encode_int(self.id))

            self._object_id = buffer_stream.BufferStream(answer.data).get_int()

        return self._agent.vm.get_object(self._object_id)

    def get_source_files(self):
        if self._source_files is None:
            answer = self._agent.send_command(
                constants.CMDSET_TYPE,
                constants.CMD_TYPE_GET_SOURCE_FILES,
                sdbtypes.encode_int(self.id))

            self._source_files = (
                buffer_stream.BufferStream(answer.data).get_array(sdbtypes.decode_string))

        return self._source_files

    def get_fields(self):
        if self._fields is None:
            def decode_field_info(buffer):
                field_id = sdbtypes.decode_int(buffer).object
                field_name, name_length = sdbtypes.decode_string(buffer[4:])
                field_type_id = (
                    sdbtypes.decode_int(buffer[4 + name_length:]).object)
                field_attrs = (
                    sdbtypes.decode_int(buffer[8 + name_length:]).object)
                mirror = field_mirror.FieldMirror(
                    self._agent, self.id,
                    field_id, field_name, field_type_id, field_attrs)

                return sdbtypes.DecodeInfo(mirror, name_length + 12)

            answer = self._agent.send_command(
                constants.CMDSET_TYPE,
                constants.CMD_TYPE_GET_FIELDS,
                sdbtypes.encode_int(self.id))

            self._fields = buffer_stream.BufferStream(answer.data).get_array(
                decode_field_info)

        return self._fields

    def get_static_field_value(self, field):
        return self.get_static_fields_values([field])[0]

    def get_static_fields_values(self, fields):
        ids = [f.id for f in fields]
        ids_encoded = sdbtypes.encode_array(ids, sdbtypes.encode_int)
        answer = self._agent.send_command(
            constants.CMDSET_TYPE,
            constants.CMD_TYPE_GET_VALUES,
            sdbtypes.encode_int(self.id) + ids_encoded)

        values = buffer_stream.BufferStream(answer.data).get_array_known_size(
            sdbtypes.decode_variant_value, len(fields))
        return values

    def set_static_field_value(self, field, value):
        self.set_static_fields_values([(field, value)])

    def set_static_fields_values(self, fields_values):
        def encode_field_value(value):
            return (
                sdbtypes.encode_int(value[0].id) +
                sdbtypes.encode_variant_value(value[1]))

        self._agent.send_command(
            constants.CMDSET_TYPE,
            constants.CMD_TYPE_SET_VALUES,
            sdbtypes.encode_int(self.id) +
            sdbtypes.encode_array(fields_values, encode_field_value))

    def get_field_by_name(self, name):
        for field in self.get_fields():
            if field.name == name:
                return field
        return None

    def get_properties(self):
        if self._properties is None:
            def decode_property(buffer):
                id = sdbtypes.decode_int(buffer).object
                name, name_length = sdbtypes.decode_string(buffer[4:])
                getter_id = sdbtypes.decode_int(
                    buffer[4 + name_length:]).object
                setter_id = sdbtypes.decode_int(
                    buffer[8 + name_length:]).object
                attrs = sdbtypes.decode_int(buffer[12 + name_length:]).object

                mirror = property_mirror.PropertyMirror(
                    self._agent, id, self.id, name,
                    getter_id, setter_id, attrs)
                return sdbtypes.DecodeInfo(mirror, 16)

            answer = self._agent.send_command(
                constants.CMDSET_TYPE,
                constants.CMD_TYPE_GET_PROPERTIES,
                sdbtypes.encode_int(self.id))

            self._properties = buffer_stream.BufferStream(answer.data).get_array(
                decode_property)

        return self._properties

    def is_assignable_from(self, other_type):
        params = (
            sdbtypes.encode_int(self.id) +
            sdbtypes.encode_int(other_type.id))
        answer = self._agent.send_command(
            constants.CMDSET_TYPE,
            constants.CMD_TYPE_IS_ASSIGNABLE_FROM,
            params)

        result = (buffer_stream.BufferStream(answer.data).get_byte() == 1)
        return result

    # Attrs

    def get_attrs(self):
        return self._get_info().attrs

    def is_abstract(self):
        return (self.get_attrs() & constants.TYPE_ATTR_ABSTRACT) != 0

    def is_import(self):
        return (self.get_attrs() & constants.TYPE_ATTR_IMPORT) != 0

    def is_interface(self):
        return (
            (self.get_attrs() & constants.TYPE_ATTR_CLASS_SEMANTICS_MASK) ==
            constants.TYPE_ATTR_INTERFACE)

    def is_sealed(self):
        return (self.get_attrs() & constants.TYPE_ATTR_SEALED) != 0

    def is_serializable(self):
        return (self.get_attrs() & constants.TYPE_ATTR_SERIALIZABLE) != 0

    def is_special_name(self):
        return (self.get_attrs() & constants.TYPE_ATTR_SPECIAL_NAME) != 0

    def is_ansi_class(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_STRING_FORMAT_MASK) ==
            constants.TYPE_ATTR_ANSI_CLASS)

    def is_unicode_class(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_STRING_FORMAT_MASK) ==
            constants.TYPE_ATTR_UNICODE_CLASS)

    def is_auto_class(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_STRING_FORMAT_MASK) ==
            constants.TYPE_ATTR_AUTO_CLASS)

    def is_auto_layout(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_LAYOUT_MASK) ==
            constants.TYPE_ATTR_AUTO_LAYOUT)

    def is_explicit_layout(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_LAYOUT_MASK) ==
            constants.TYPE_ATTR_EXPLICIT_LAYOUT)

    def is_layout_sequential(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_LAYOUT_MASK) ==
            constants.TYPE_ATTR_SEQUENTIAL_LAYOUT)

    def is_nested_assembly(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_NESTED_ASSEMBLY)

    def is_nested_fam_and_assem(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_NESTED_FAM_AND_ASSEM)

    def is_nested_family(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_NESTED_FAMILY)

    def is_nested_fam_or_assem(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_NESTED_FAM_OR_ASSEM)

    def is_nested_private(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_NESTED_PRIVATE)

    def is_nested_public(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_NESTED_PUBLIC)

    def is_not_public(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_NOT_PUBLIC)

    def is_public(self):
        return ((self.get_attrs() & constants.TYPE_ATTR_VISIBILITY_MASK) ==
            constants.TYPE_ATTR_PUBLIC)

    def is_array(self):
        return self.get_rank() > 0

    def is_enum(self):
        return self._get_info().is_enum

    def is_pointer(self):
        return self._get_info().is_pointer

    def is_primitive(self):
        return self._get_info().is_primitive

    def is_value_type(self):
        return self._get_info().is_value_type

    def is_marshal_byref(self):
        return self._get_info().is_marshal_byref

    def is_class(self):
        return (not self.is_interface()) and (not self.is_value_type())

    def _get_info(self):
        if self._info is None:
            answer = self._agent.send_command(
                constants.CMDSET_TYPE,
                constants.CMD_TYPE_GET_INFO,
                sdbtypes.encode_int(self.id))

            stream = buffer_stream.BufferStream(answer.data)
            namespace = stream.get_string()
            name = stream.get_string()
            fullname = stream.get_string()
            assembly_id = stream.get_int()
            module_id = stream.get_int()
            base_type_id = stream.get_int()
            underlying_type_id = stream.get_int()
            token = stream.get_int()
            rank = stream.get_byte()
            attrs = stream.get_int()
            flags = stream.get_byte()
            is_marshal_byref = (flags & 1) != 0
            is_pointer = (flags & 2) != 0
            is_primitive = (flags & 4) != 0
            is_value_type = (flags & 8) != 0
            is_enum = (flags & 16) != 0
            nested_types_ids = stream.get_array(sdbtypes.decode_int)

            self._info = TypeInfo(
                namespace, name, fullname,
                assembly_id, module_id, base_type_id,
                underlying_type_id, token, rank,
                attrs, is_marshal_byref, is_pointer, is_primitive,
                is_value_type, is_enum, nested_types_ids)

        return self._info
