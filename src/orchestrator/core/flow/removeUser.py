import logging

from orchestrator.core.idm import IdMOperations

logger = logging.getLogger('orchestrator_core')


class RemoveUser(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

    def removeUser_impl(self,
                        SERVICE_NAME,
                        SERVICE_ADMIN_USER,
                        SERVICE_ADMIN_PASSWORD,
                        SERVICE_ADMIN_TOKEN,
                        USER_NAME):

        '''Removes an user Service (aka domain user keystone).
        
        In case of HTTP error, return HTTP error
        
        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - USER_NAME: User name
        '''
    
        try:
            if not SERVICE_ADMIN_TOKEN: 
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 2. Get user ID
            #
            ID_USER = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                               USER_NAME)
            logger.debug("ID of user %s: %s" % (USER_NAME, ID_USER))


            # TODO: disable us before remove it ?
        
            #
            # 3. Remove user ID
            #
            self.idm.removeUser(SERVICE_ADMIN_TOKEN,
                                ID_USER)
            #logger.debug("ID of user %s: %s" % (USER_NAME, ID_USER))


        except Exception, ex:
            logger.error(ex)
            return { "error": str(ex) }
    
        logger.info("Summary report:")
        logger.info("ID_USER=%s" % ID_USER)

        #return {"id":ID_USER}




