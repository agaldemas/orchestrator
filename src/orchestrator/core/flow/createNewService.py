#
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of IoT orchestrator
#
# IoT orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# IoT orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with IoT orchestrator. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT team
#
import logging
import sys
import os
import json

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class CreateNewService(FlowBase):

    def createNewService(self,
                         DOMAIN_NAME,
                         DOMAIN_ADMIN_USER,
                         DOMAIN_ADMIN_PASSWORD,
                         DOMAIN_ADMIN_TOKEN,
                         NEW_SERVICE_NAME,
                         NEW_SERVICE_DESCRIPTION,
                         NEW_SERVICE_ADMIN_USER,
                         NEW_SERVICE_ADMIN_PASSWORD,
                         NEW_SERVICE_ADMIN_EMAIL):

        '''Creates a new Service (aka domain keystone).

        In case of HTTP error, return HTTP error

        Params:
        - DOMAIN_NAME: Domain name
        - DOMAIN_ADMIN_USER: admin user name in domain
        - DOMAIN_ADMIN_PASSWORD: admin password in domain
        - DOMAIN_ADMIN_TOKEN: admin user token in domain
        - NEW_SERVICE_NAME: New service name
        - NEW_SERVICE_DESCRIPTION: New service description
        - NEW_SERVICE_ADMIN_USER: New service admin username
        - NEW_SERVICE_ADMIN_PASSWORD: New service admin password
        - NEW_SERVICE_ADMIN_EMAIL: New service admin password (optional)
        Return:
        - token: service admin token
        - id: service Id
        '''

        SUB_SERVICE_ADMIN_ROLE_NAME = "SubServiceAdmin"
        SUB_SERVICE_CUSTOMER_ROLE_NAME = "SubServiceCustomer"

        data_log = {
            "DOMAIN_NAME": "%s" % DOMAIN_NAME,
            "DOMAIN_ADMIN_USER": "%s" % DOMAIN_ADMIN_USER,
            "DOMAIN_ADMIN_PASSWORD": "%s" % DOMAIN_ADMIN_PASSWORD,
            "DOMAIN_ADMIN_TOKEN": "%s" % DOMAIN_ADMIN_TOKEN,
            "NEW_SERVICE_NAME": "%s" % NEW_SERVICE_NAME,
            "NEW_SERVICE_DESCRIPTION": "%s" % NEW_SERVICE_DESCRIPTION,
            "NEW_SERVICE_ADMIN_USER": "%s" % NEW_SERVICE_ADMIN_PASSWORD
        }
        logger.debug("createNewService invoked with: %s" % json.dumps(
            data_log,
            indent=3)
            )
        try:

            if not DOMAIN_ADMIN_TOKEN:
                DOMAIN_ADMIN_TOKEN = self.idm.getToken(DOMAIN_NAME,
                                                       DOMAIN_ADMIN_USER,
                                                       DOMAIN_ADMIN_PASSWORD)
            logger.debug("DOMAIN_ADMIN_TOKEN=%s" % DOMAIN_ADMIN_TOKEN)

            #
            # 1. Create service (aka domain)
            #
            ID_DOM1 = self.idm.createDomain(DOMAIN_ADMIN_TOKEN,
                                            NEW_SERVICE_NAME,
                                            NEW_SERVICE_DESCRIPTION)
            logger.debug("ID of your new service %s:%s" % (NEW_SERVICE_NAME,
                                                           ID_DOM1))

            #
            # 2. Create user admin for new service (aka domain)
            #
            try:
                ID_ADM1 = self.idm.createUserDomain(DOMAIN_ADMIN_TOKEN,
                                                ID_DOM1,
                                                NEW_SERVICE_NAME,
                                                NEW_SERVICE_ADMIN_USER,
                                                NEW_SERVICE_ADMIN_PASSWORD,
                                                NEW_SERVICE_ADMIN_EMAIL,
                                                None)
            except Exception, ex:
                logger.debug("ERROR creating user %s: %s" % (
                    NEW_SERVICE_ADMIN_USER,
                    ex))
                logger.debug("removing uncomplete created domain %s" % ID_DOM1)
                self.idm.disableDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
                self.idm.deleteDomain(DOMAIN_ADMIN_TOKEN, ID_DOM1)
                return self.composeErrorCode(ex)

            logger.debug("ID of user %s: %s" % (NEW_SERVICE_ADMIN_USER,
                                                ID_ADM1))

            #
            # 3. Grant Admin role to $NEW_SERVICE_ADMIN_USER of new service
            #
            ADMIN_ROLE_ID = self.idm.getRoleId(DOMAIN_ADMIN_TOKEN,
                                               ROLE_NAME="admin")
            logger.debug("ID of role  %s: %s" % ("admin",
                                                 ID_ADM1))

            self.idm.grantDomainRole(DOMAIN_ADMIN_TOKEN, ID_DOM1, ID_ADM1,
                                     ADMIN_ROLE_ID)

            NEW_SERVICE_ADMIN_TOKEN = self.idm.getToken(
                NEW_SERVICE_NAME,
                NEW_SERVICE_ADMIN_USER,
                NEW_SERVICE_ADMIN_PASSWORD)
            logger.debug("NEW_SERVICE_ADMIN_TOKEN %s" % NEW_SERVICE_ADMIN_TOKEN)

            #
            # 4. Create SubService roles
            #
            ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN = self.idm.createDomainRole(
                NEW_SERVICE_ADMIN_TOKEN,
                SUB_SERVICE_ADMIN_ROLE_NAME,
                ID_DOM1)
            logger.debug("ID of role %s: %s" % (SUB_SERVICE_ADMIN_ROLE_NAME,
                                                ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN))

            ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER = self.idm.createDomainRole(
                NEW_SERVICE_ADMIN_TOKEN,
                SUB_SERVICE_CUSTOMER_ROLE_NAME,
                ID_DOM1)
            logger.debug("ID of role %s: %s" % (SUB_SERVICE_CUSTOMER_ROLE_NAME,
                                                ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER))

            #
            # 4.5 Inherit subserviceadim
            #
            self.idm.grantInheritRole(NEW_SERVICE_ADMIN_TOKEN,
                                      ID_DOM1,
                                      ID_ADM1,
                                      ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN)
            #
            # 5. Provision default platform roles AccessControl policies
            #
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-orion-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-perseo-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-iotagent-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
                                    POLICY_FILE_NAME='policy-sth-admin.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-orion-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-perseo-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-iotagent-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER,
                                    POLICY_FILE_NAME='policy-sth-customer.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-orion-admin2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-perseo-admin2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-iotagent-admin2.xml')
            self.ac.provisionPolicy(NEW_SERVICE_NAME, NEW_SERVICE_ADMIN_TOKEN,
                                    ADMIN_ROLE_ID,
                                    POLICY_FILE_NAME='policy-sth-admin2.xml')

        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)

        data_log = {
            "ID_DOM1": "%s" % ID_DOM1,
            "NEW_SERVICE_ADMIN_TOKEN": "%s" % NEW_SERVICE_ADMIN_TOKEN,
            "ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN": "%s" % ID_NEW_SERVICE_ROLE_SUBSERVICEADMIN,
            "ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER": "%s" % ID_NEW_SERVICE_ROLE_SUBSERVICECUSTOMER
        }
        logger.info("Summary report : %s" % json.dumps(data_log, indent=3))

        return {
            "token": NEW_SERVICE_ADMIN_TOKEN,
            "id": ID_DOM1,
        }
