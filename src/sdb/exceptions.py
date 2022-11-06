import constants

class InvalidObjectError(Exception):
    pass

class InvalidFieldIdError(Exception):
    pass

class InvalidFrameIdError(Exception):
    pass

class FeatureIsNotImplementedError(Exception):
    pass

class VmIsNotSuspendedError(Exception):
    pass

class InvalidArgumentError(Exception):
    pass

class ObjectIsUnloadedError(Exception):
    pass

class NoInvocationError(Exception):
    pass

class AbsentInformationError(Exception):
    pass

class WrongILOffsetError(Exception):
    pass

class ExecutableNotFound(Exception):
    pass

class ExitException(Exception):
    pass

def error_code_to_exception(error_code):
    if error_code == constants.RESULT_INVALID_OBJECT:
        return InvalidObjectError()
    elif error_code == constants.RESULT_INVALID_FIELD_ID:
        return InvalidFieldIdError()
    elif error_code == constants.RESULT_INVALID_FRAME_ID:
        return InvalidFrameIdError()
    elif error_code == constants.RESULT_NOT_IMPLEMENTED:
        return FeatureIsNotImplementedError()
    elif error_code == constants.RESULT_NOT_SUSPENDED:
        return VmIsNotSuspendedError()
    elif error_code == constants.RESULT_INVALID_ARGUMENT:
        return InvalidArgumentError()
    elif error_code == constants.RESULT_UNLOADED:
        return ObjectIsUnloadedError()
    elif error_code == constants.RESULT_NO_INVOCATION:
        return NoInvocationError()
    elif error_code == constants.RESULT_ABSENT_INFORMATION:
        return AbsentInformationError()
    elif error_code == constants.RESULT_WRONG_IL_OFFSET:
        return WrongILOffsetError()
    elif error_code == constants.RESULT_SUCCESS:
        return None
    else:
        assert False, "Unknown error code"
