import logging
import json
from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class CreateTrustToken(FlowBase):

    def createTrustToken(self,
                         SERVICE_NAME,
                         SERVICE_ID,
                         SUBSERVICE_NAME,
                         SUBSERVICE_ID,
                         SERVICE_ADMIN_USER,
                         SERVICE_ADMIN_PASSWORD,
                         SERVICE_ADMIN_TOKEN,
                         ROLE_NAME,
                         ROLE_ID,
                         TRUSTEE_USER_NAME,
                         TRUSTEE_USER_ID,
                         TRUSTOR_USER_NAME,
                         TRUSTOR_USER_ID):

        '''Creates a trust token

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ID: Service Id
        - SUBSERVICE_NAME: SubService name
        - SUBSERVICE_ID: SubService Id
        - SERVICE_ADMIN_USER: Service admin token
        - SERVICE_ADMIN_PASSWORD: Service admin token
        - SERVICE_ADMIN_TOKEN: Service admin token
        - ROLE_NAME: Role name
        - ROLE_ID: Role name
        - TRUSTEE_USER_NAME:
        - TRUSTEE_USER_ID:
        - TRUSTOR_USER_NAME:
        - TRUSTOR_USER_ID:
        Return:
        - token: Trust Token
        '''
        data_log = {
            "SERVICE_NAME":"%s" % SERVICE_NAME,
            "SERVICE_ID":"%s" % SERVICE_ID,
            "SUBSERVICE_NAME":"%s" % SUBSERVICE_NAME,
            "SUBSERVICE_ID":"%s" % SUBSERVICE_ID,
            "SERVICE_ADMIN_USER":"%s" % SERVICE_ADMIN_USER,
            "SERVICE_ADMIN_PASSWORD":"%s" % SERVICE_ADMIN_PASSWORD,
            "SERVICE_ADMIN_TOKEN":"%s" % SERVICE_ADMIN_TOKEN,
            "ROLE_NAME":"%s" % ROLE_NAME,
            "ROLE_ID":"%s" % ROLE_ID,
            "TRUSTEE_USER_NAME":"%s" % TRUSTEE_USER_NAME,
            "TRUSTEE_USER_ID":"%s" % TRUSTEE_USER_ID,
            "TRUSTOR_USER_NAME":"%s" % TRUSTOR_USER_NAME,
            "TRUSTOR_USER_ID":"%s" % TRUSTOR_USER_ID,
        }
        logger.debug("createTrustToken invoked with: %s" % json.dumps(data_log, indent=3))

        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #
            if not SERVICE_ID:
                SERVICE_ID = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                                  SERVICE_NAME)

            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, SERVICE_ID))

            #
            # 2. Get SubService (aka project)
            #
            if not SUBSERVICE_ID:
                SUBSERVICE_ID = self.idm.getProjectId(SERVICE_ADMIN_TOKEN,
                                                      SERVICE_NAME,
                                                      SUBSERVICE_NAME)
            logger.debug("ID of your subservice %s:%s" % (SUBSERVICE_NAME, SUBSERVICE_ID))

            #
            # 3. Get role
            #
            if not ROLE_ID:
                ROLE_ID = self.idm.getDomainRoleId(SERVICE_ADMIN_TOKEN,
                                                   SERVICE_ID,
                                                   ROLE_NAME)
            logger.debug("ID of role %s: %s" % (ROLE_NAME, ROLE_ID))


            #
            # 4. Get Trustee User
            #
            if not TRUSTEE_USER_ID:
                # We are asuming that trustee belong to SERVICE!!
                TRUSTEE_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           TRUSTEE_USER_NAME)
            logger.debug("ID of trustee user %s: %s" % (TRUSTEE_USER_NAME, TRUSTEE_USER_ID))

            #
            # 5. Get Trustor User
            #
            if not TRUSTOR_USER_ID:
                TRUSTOR_USER_ID = self.idm.getDomainUserId(SERVICE_ADMIN_TOKEN,
                                                           SERVICE_ID,
                                                           TRUSTOR_USER_NAME)
            logger.debug("ID of trustor user %s: %s" % (TRUSTOR_USER_NAME, TRUSTOR_USER_ID))


            #
            # 6. Create trust
            #
            ID_TRUST = self.idm.createTrustToken(SERVICE_ADMIN_TOKEN,
                                                 SUBSERVICE_ID,
                                                 ROLE_ID,
                                                 TRUSTEE_USER_ID,
                                                 TRUSTOR_USER_ID)

            logger.debug("ID of Trust %s" % (ID_TRUST))


                
        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)


        data_log = {
            "ID_TRUST":"%s" % ID_TRUST
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {"id": ID_TRUST}

