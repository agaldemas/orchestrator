import logging

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class Projects(FlowBase):

    def projects(self,
                DOMAIN_ID,
                DOMAIN_NAME,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Get Projects of a domain.

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - DOMAIN_NAME: name of domain
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - project array list
        '''
        logger.debug("projects invoked with: ")
        logger.debug("DOMAIN_ID=%s" % DOMAIN_ID)
        logger.debug("DOMAIN_NAME=%s" % DOMAIN_NAME)
        logger.debug("ADMIN_USER=%s" % ADMIN_USER)
        logger.debug("ADMIN_PASSWORD=%s" % ADMIN_PASSWORD)
        logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

        try:
            if not ADMIN_TOKEN:
                if not DOMAIN_ID:
                    import ipdb
                    ipdb.set_trace()
                    ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                    ADMIN_USER,
                                                    ADMIN_PASSWORD)
                    DOMAIN_ID = self.idm.getDomainId(ADMIN_TOKEN,
                                                     DOMAIN_NAME)

                else:
                    ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                     ADMIN_USER,
                                                     ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)


            PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
                                                  DOMAIN_ID)

            logger.debug("PROJECTS=%s" % PROJECTS)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("PROJECTS=%s" % PROJECTS)

        return PROJECTS

    def get_project(self,
                DOMAIN_ID,
                PROJECT_ID,
                ADMIN_USER,
                ADMIN_PASSWORD,
                ADMIN_TOKEN):

        '''Ge Project detail of a domain

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_ID: id of domain
        - PROJECT_ID: id of project
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        Return:
        - project detail
        '''
        logger.debug("get_project invoked with: ")
        logger.debug("DOMAIN_ID=%s" % DOMAIN_ID)
        logger.debug("PROJECT_ID=%s" % PROJECT_ID)
        logger.debug("ADMIN_USER=%s" % ADMIN_USER)
        logger.debug("ADMIN_PASSWORD=%s" % ADMIN_PASSWORD)
        logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

        try:
            if not ADMIN_TOKEN:
                ADMIN_TOKEN = self.idm.getToken2(DOMAIN_ID,
                                                ADMIN_USER,
                                                ADMIN_PASSWORD)
            logger.debug("ADMIN_TOKEN=%s" % ADMIN_TOKEN)

            PROJECT = self.idm.getProject(ADMIN_TOKEN,
                                          PROJECT_ID)
            # PROJECTS = self.idm.getDomainProjects(ADMIN_TOKEN,
            #                                       DOMAIN_ID)
            # for project in PROJECTS:
            #     if project['id'] == PROJECT_ID:
            #         PROJECT = project

            logger.debug("PROJECT=%s" % PROJECT)

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        logger.info("Summary report:")
        logger.info("PROJECT=%s" % PROJECT)

        return PROJECT


