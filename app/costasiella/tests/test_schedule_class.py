# from graphql.error.located_error import GraphQLLocatedError
import graphql
import base64
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene.test import Client
from graphql_relay import to_global_id

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, Permission

from . import factories as f
from .helpers import execute_test_client_api_query
from .. import models
from .. import schema


class GQLScheduleClass(TestCase):
    # https://docs.djangoproject.com/en/2.1/topics/testing/overview/

    def setUp(self):
        # This is run before every test
        self.admin_user = f.AdminUserFactory.create()
        self.anon_user = AnonymousUser()

        self.permission_view = 'view_scheduleclass'
        self.permission_add = 'add_scheduleclass'
        self.permission_change = 'change_scheduleclass'
        self.permission_delete = 'delete_scheduleclass'


        a_monday = datetime.date(2019, 6, 17)
        self.variables_query_list = {
            'dateFrom': str(a_monday),
            'dateUntil': str(a_monday + datetime.timedelta(days=6))
        }

        self.organization_location_room = f.OrganizationLocationRoomFactory.create()
        self.organization_classtype = f.OrganizationClasstypeFactory.create()
        self.organization_level = f.OrganizationLevelFactory.create()

        self.variables_create = {
            "input": {
                "frequencyType": "WEEKLY",
                "frequencyInterval": 1, # Monday,
                "organizationLocationRoom": to_global_id('OrganizationLocationRoomNode', self.organization_location_room.id),
                "organizationClasstype": to_global_id('OrganizationClasstypeNode', self.organization_classtype.id),
                "organizationLevel": to_global_id('OrganizationLevelNode', self.organization_level.id),
                "dateStart": "2019-01-01",
                "dateEnd": "2999-12-31",
                "timeStart": "11:00:00",
                "timeEnd": "12:30:00",
                "displayPublic": True
            }
        }

        self.variables_update = {
            "input": {
                "frequencyType": "WEEKLY",
                "frequencyInterval": 2, # Tuesday,
                "organizationLocationRoom": to_global_id('OrganizationLocationRoomNode', self.organization_location_room.id),
                "organizationClasstype": to_global_id('OrganizationClasstypeNode', self.organization_classtype.id),
                "organizationLevel": to_global_id('OrganizationLevelNode', self.organization_level.id),
                "dateStart": "1999-01-01",
                "dateEnd": "2999-12-31",
                "timeStart": "16:00:00",
                "timeEnd": "17:30:00",
                "displayPublic": True
            }
        }

        self.variables_delete = {
            "input": {}
        }

        self.scheduleclasses_query = '''
  query ScheduleClasses($dateFrom: Date!, $dateUntil:Date!) {
    scheduleClasses(dateFrom:$dateFrom, dateUntil: $dateUntil) {
      date
      classes {
        scheduleItemId
        frequencyType
        date
        organizationLocationRoom {
          id
          name
          organizationLocation {
            id
            name
          }
        }
        organizationClasstype {
          id
          name
        }
        organizationLevel {
          id
          name
        }
        timeStart
        timeEnd
        displayPublic
      }
    }
  }
'''

        self.scheduleclass_query = '''
  query ScheduleItem($id: ID!) {
    scheduleItem(id:$id) {
      id
      frequencyType
      frequencyInterval
      organizationLocationRoom {
        id
        name
      }
      organizationClasstype {
        id
        name
      }
      organizationLevel {
        id
        name
      }
      dateStart
      dateEnd
      timeStart
      timeEnd
      displayPublic
    }
  }
'''

        self.scheduleclass_create_mutation = ''' 
  mutation CreateScheduleClass($input:CreateScheduleClassInput!) {
    createScheduleClass(input: $input) {
      scheduleItem {
        id
        scheduleItemType
        frequencyType
        frequencyInterval
        organizationLocationRoom {
          id
          name
          organizationLocation {
            id
            name
          }
        }
        organizationClasstype {
          id
          name
        }
        organizationLevel {
          id
          name
        }
        dateStart
        dateEnd
        timeStart
        timeEnd
        displayPublic
      }
    }
  }
'''

        self.scheduleclass_update_mutation = '''
  mutation UpdateScheduleClass($input:UpdateScheduleClassInput!) {
    updateScheduleClass(input: $input) {
      scheduleItem {
        id
        scheduleItemType
        frequencyType
        frequencyInterval
        organizationLocationRoom {
          id
          name
          organizationLocation {
            id
            name
          }
        }
        organizationClasstype {
          id
          name
        }
        organizationLevel {
          id
          name
        }
        dateStart
        dateEnd
        timeStart
        timeEnd
        displayPublic
      }
    }
  }
'''

        self.scheduleclass_delete_mutation = '''
  mutation DeleteScheduleClass($input: DeleteScheduleClassInput!) {
    deleteScheduleClass(input: $input) {
      ok
    }
  }
'''

    def tearDown(self):
        # This is run after every test
        pass


    def test_query_input_validation_error_dateUntil_smaller_then_dateFrom(self):
        """ Query list of scheduleclasses 
        An error message should be returned if dateUntil < dateFrom
        """
        query = self.scheduleclasses_query
        
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()
        a_monday = datetime.date(2019, 6, 17)
        variables = {
            'dateFrom': str(a_monday),
            'dateUntil': str(a_monday - datetime.timedelta(days=6))
        }

        executed = execute_test_client_api_query(query, self.admin_user, variables=variables)
        errors = executed.get('errors')       

        self.assertEqual(errors[0]['message'], 'dateUntil has to be bigger then dateFrom')


    def test_query_input_validation_error_date_input_max_7_days_apart(self):
        """ Query list of scheduleclasses 
        An error message should be returned if dates apart > 7 days
        """
        query = self.scheduleclasses_query
        
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()
        a_monday = datetime.date(2019, 6, 17)
        variables = {
            'dateFrom': str(a_monday),
            'dateUntil': str(a_monday + datetime.timedelta(days=31))
        }

        executed = execute_test_client_api_query(query, self.admin_user, variables=variables)
        errors = executed.get('errors')

        self.assertEqual(errors[0]['message'], "dateFrom and dateUntil can't be more then 7 days apart")


    def test_query(self):
        """ Query list of scheduleclasses """
        query = self.scheduleclasses_query
        
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()

        variables = self.variables_query_list
        executed = execute_test_client_api_query(query, self.admin_user, variables=variables)
        data = executed.get('data')

        self.assertEqual(data['scheduleClasses'][0]['date'], variables['dateFrom'])
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['scheduleItemId'], 
            to_global_id('ScheduleItemNode', schedule_class.id)
        )
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['organizationClasstype']['id'], 
            to_global_id('OrganizationClasstypeNode', schedule_class.organization_classtype.id)
        )
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['organizationLocationRoom']['id'], 
            to_global_id('OrganizationLocationRoomNode', schedule_class.organization_location_room.id)
        )
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['organizationLevel']['id'], 
            to_global_id('OrganizationLevelNode', schedule_class.organization_level.id)
        )
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['timeStart'], 
            str(schedule_class.time_start)
        )
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['timeEnd'], 
            str(schedule_class.time_end)
        )
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['displayPublic'], 
            schedule_class.display_public
        )


    def test_query_permision_denied(self):
        """ Query list of scheduleclasses - check permission denied """
        query = self.scheduleclasses_query
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()

        # Create regular user
        user = f.RegularUserFactory.create()
        executed = execute_test_client_api_query(query, user, variables=self.variables_query_list)
        errors = executed.get('errors')

        self.assertEqual(errors[0]['message'], 'Permission denied!')


    def test_query_permision_granted(self):
        """ Query list of scheduleclasses with view permission """
        query = self.scheduleclasses_query
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()

        # Create regular user
        user = f.RegularUserFactory.create()
        permission = Permission.objects.get(codename='view_scheduleclass')
        user.user_permissions.add(permission)
        user.save()

        variables = self.variables_query_list
        executed = execute_test_client_api_query(query, user, variables=variables)
        data = executed.get('data')

        # List all scheduleclasses
        self.assertEqual(data['scheduleClasses'][0]['date'], variables['dateFrom'])
        self.assertEqual(
            data['scheduleClasses'][0]['classes'][0]['scheduleItemId'], 
            to_global_id('ScheduleItemNode', schedule_class.id)
        )


    def test_query_anon_user(self):
        """ Query list of scheduleclasses - anon user """
        query = self.scheduleclasses_query
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()

        executed = execute_test_client_api_query(query, self.anon_user, variables=self.variables_query_list)
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Not logged in!')


    def test_query_one(self):
        """ Query one schedule_item as admin """   
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()
        node_id = to_global_id('ScheduleItemNode', schedule_class.id)

        # Now query single schedule item and check
        executed = execute_test_client_api_query(self.scheduleclass_query, self.admin_user, variables={"id": node_id})
        data = executed.get('data')

        self.assertEqual(data['scheduleItem']['id'], node_id)
        self.assertEqual(data['scheduleItem']['frequencyType'], schedule_class.frequency_type)
        self.assertEqual(data['scheduleItem']['frequencyInterval'], schedule_class.frequency_interval)
        self.assertEqual(
          data['scheduleItem']['organizationLocationRoom']['id'], 
          to_global_id('OrganizationLocationRoomNode', schedule_class.organization_location_room.id)
        )
        self.assertEqual(
          data['scheduleItem']['organizationClasstype']['id'], 
          to_global_id('OrganizationClasstypeNode', schedule_class.organization_classtype.id)
        )
        self.assertEqual(
          data['scheduleItem']['organizationLevel']['id'], 
          to_global_id('OrganizationLevelNode', schedule_class.organization_level.id)
        )
        self.assertEqual(data['scheduleItem']['dateStart'], str(schedule_class.date_start))
        self.assertEqual(data['scheduleItem']['dateEnd'], str(schedule_class.date_end))
        self.assertEqual(data['scheduleItem']['timeStart'], str(schedule_class.time_start))
        self.assertEqual(data['scheduleItem']['timeEnd'], str(schedule_class.time_end))
        self.assertEqual(data['scheduleItem']['displayPublic'], schedule_class.display_public)


    def test_query_one_anon_user(self):
        """ Deny permission for anon users Query one glacount """   
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()
        node_id = to_global_id('ScheduleItemNode', schedule_class.id)

        # Now query single scheduleclass and check
        executed = execute_test_client_api_query(self.scheduleclass_query, self.anon_user, variables={"id": node_id})
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Not logged in!')


    def test_query_one_permission_denied(self):
        """ Permission denied message when user lacks authorization """   
        # Create regular user
        user = f.RegularUserFactory.create()

        schedule_class = f.SchedulePublicWeeklyClassFactory.create()
        node_id = to_global_id('ScheduleItemNode', schedule_class.id)

        # Now query single scheduleclass and check
        executed = execute_test_client_api_query(self.scheduleclass_query, user, variables={"id": node_id})
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Permission denied!')


    def test_query_one_permission_granted(self):
        """ Respond with data when user has permission """   
        user = f.RegularUserFactory.create()
        permission = Permission.objects.get(codename='view_scheduleclass')
        user.user_permissions.add(permission)
        user.save()
        
        schedule_class = f.SchedulePublicWeeklyClassFactory.create()
        node_id = to_global_id('ScheduleItemNode', schedule_class.id)

        # Now query single location and check   
        executed = execute_test_client_api_query(self.scheduleclass_query, user, variables={"id": node_id})
        data = executed.get('data')
        self.assertEqual(data['scheduleItem']['id'], node_id)


    def test_create_scheduleclass(self):
        """ Create a scheduleclass """
        query = self.scheduleclass_create_mutation
        variables = self.variables_create

        executed = execute_test_client_api_query(
            query, 
            self.admin_user, 
            variables=variables
        )
        
        data = executed.get('data')
        self.assertEqual(data['createScheduleClass']['scheduleItem']['frequencyType'], variables['input']['frequencyType'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['frequencyInterval'], variables['input']['frequencyInterval'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['organizationLocationRoom']['id'], variables['input']['organizationLocationRoom'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['organizationClasstype']['id'], variables['input']['organizationClasstype'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['organizationLevel']['id'], variables['input']['organizationLevel'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['dateStart'], variables['input']['dateStart'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['dateEnd'], variables['input']['dateEnd'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['timeStart'], variables['input']['timeStart'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['timeEnd'], variables['input']['timeEnd'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['displayPublic'], variables['input']['displayPublic'])


    def test_create_scheduleclass_anon_user(self):
        """ Don't allow creating scheduleclasses for non-logged in users """
        query = self.scheduleclass_create_mutation
        variables = self.variables_create

        executed = execute_test_client_api_query(
            query, 
            self.anon_user, 
            variables=variables
        )
        data = executed.get('data')
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Not logged in!')


    def test_create_location_permission_granted(self):
        """ Allow creating scheduleclasses for users with permissions """
        query = self.scheduleclass_create_mutation
        variables = self.variables_create

        # Create regular user
        user = f.RegularUserFactory.create()
        permission = Permission.objects.get(codename=self.permission_add)
        user.user_permissions.add(permission)
        user.save()

        executed = execute_test_client_api_query(
            query, 
            user, 
            variables=variables
        )
        data = executed.get('data')
        self.assertEqual(data['createScheduleClass']['scheduleItem']['frequencyType'], variables['input']['frequencyType'])
        self.assertEqual(data['createScheduleClass']['scheduleItem']['frequencyInterval'], variables['input']['frequencyInterval'])


    def test_create_scheduleclass_permission_denied(self):
        """ Check create scheduleclass permission denied error message """
        query = self.scheduleclass_create_mutation
        variables = self.variables_create

        # Create regular user
        user = f.RegularUserFactory.create()

        executed = execute_test_client_api_query(
            query, 
            user, 
            variables=variables
        )
        data = executed.get('data')
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Permission denied!')


    def test_update_scheduleclass(self):
        """ Update a scheduleclass """
        query = self.scheduleclass_update_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_update
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)

        executed = execute_test_client_api_query(
            query, 
            self.admin_user, 
            variables=variables
        )
        data = executed.get('data')
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['id'], variables['input']['id'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['frequencyType'], variables['input']['frequencyType'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['frequencyInterval'], variables['input']['frequencyInterval'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['organizationLocationRoom']['id'], variables['input']['organizationLocationRoom'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['organizationClasstype']['id'], variables['input']['organizationClasstype'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['organizationLevel']['id'], variables['input']['organizationLevel'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['dateStart'], variables['input']['dateStart'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['dateEnd'], variables['input']['dateEnd'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['timeStart'], variables['input']['timeStart'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['timeEnd'], variables['input']['timeEnd'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['displayPublic'], variables['input']['displayPublic'])


    def test_update_scheduleclass_anon_user(self):
        """ Don't allow updating scheduleclasses for non-logged in users """
        query = self.scheduleclass_update_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_update
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)

        executed = execute_test_client_api_query(
            query, 
            self.anon_user, 
            variables=variables
        )
        data = executed.get('data')
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Not logged in!')


    def test_update_scheduleclass_permission_granted(self):
        """ Allow updating scheduleclasses for users with permissions """
        query = self.scheduleclass_update_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_update
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)

        # Create regular user
        user = f.RegularUserFactory.create()
        permission = Permission.objects.get(codename=self.permission_change)
        user.user_permissions.add(permission)
        user.save()

        executed = execute_test_client_api_query(
            query, 
            user, 
            variables=variables
        )
        data = executed.get('data')
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['id'], variables['input']['id'])
        self.assertEqual(data['updateScheduleClass']['scheduleItem']['frequencyType'], variables['input']['frequencyType'])


    def test_update_scheduleclass_permission_denied(self):
        """ Check update scheduleclass permission denied error message """
        query = self.scheduleclass_update_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_update
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)

        # Create regular user
        user = f.RegularUserFactory.create()

        executed = execute_test_client_api_query(
            query, 
            user, 
            variables=variables
        )
        data = executed.get('data')
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Permission denied!')


    def test_delete_scheduleclass(self):
        """ Delete a scheduleclass """
        query = self.scheduleclass_delete_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_delete
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)

        executed = execute_test_client_api_query(
            query, 
            self.admin_user, 
            variables=variables
        )
        data = executed.get('data')
        self.assertEqual(data['deleteScheduleClass']['ok'], True)


    def test_delete_scheduleclass_anon_user(self):
        """ Delete scheduleclass denied for anon user """
        query = self.scheduleclass_delete_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_delete
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)

        executed = execute_test_client_api_query(
            query, 
            self.anon_user, 
            variables=variables
        )
        data = executed.get('data')
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Not logged in!')


    def test_delete_scheduleclass_permission_granted(self):
        """ Allow deleting scheduleclasses for users with permissions """
        query = self.scheduleclass_delete_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_delete
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)

        # Create regular user
        user = f.RegularUserFactory.create()
        permission = Permission.objects.get(codename=self.permission_delete)
        user.user_permissions.add(permission)
        user.save()

        executed = execute_test_client_api_query(
            query, 
            user,
            variables=variables
        )
        data = executed.get('data')
        self.assertEqual(data['deleteScheduleClass']['ok'], True)


    def test_delete_scheduleclass_permission_denied(self):
        """ Check delete scheduleclass permission denied error message """
        query = self.scheduleclass_delete_mutation
        scheduleclass = f.SchedulePublicWeeklyClassFactory.create()
        variables = self.variables_delete
        variables['input']['id'] = to_global_id('ScheduleItemNode', scheduleclass.pk)
        
        # Create regular user
        user = f.RegularUserFactory.create()

        executed = execute_test_client_api_query(
            query, 
            user, 
            variables=variables
        )
        data = executed.get('data')
        errors = executed.get('errors')
        self.assertEqual(errors[0]['message'], 'Permission denied!')
