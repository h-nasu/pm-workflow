class PMWorkflowError(Exception):
    pass


class ExternalAPIError(PMWorkflowError):
    pass


class LLMError(PMWorkflowError):
    pass


class ValidationError(PMWorkflowError):
    pass


class NotFoundError(PMWorkflowError):
    pass
