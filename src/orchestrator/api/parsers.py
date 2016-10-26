import jsonschema
import logging
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from orchestrator.api import schemas

from orchestrator.common.util import ContextFilterCorrelatorId
from orchestrator.common.util import ContextFilterTransactionId
from orchestrator.common.util import ContextFilterService
from orchestrator.common.util import ContextFilterSubService

logger = logging.getLogger('orchestrator_api')
logger.addFilter(ContextFilterCorrelatorId("n/a"))
logger.addFilter(ContextFilterTransactionId("n/a"))
logger.addFilter(ContextFilterService("None"))
logger.addFilter(ContextFilterSubService(""))

class JSONSchemaParser(JSONParser):
 
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(stream, media_type,
                                                   parser_context)
        try:
            jsonschema.validate(
                data,
                schemas.json[parser_context['view'].schema_name])
        except (ValueError, jsonschema.exceptions.ValidationError) as error:
            logger.debug(error.message)
            raise ParseError(detail=error.message)
        else:
            return data
