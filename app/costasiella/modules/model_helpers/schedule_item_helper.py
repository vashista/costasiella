from django.db.models import Q

from ...models import OrganizationClasspassGroup, OrganizationSubscriptionGroup, \
                        ScheduleItem, ScheduleItemWeeklyOTC, \
                        ScheduleItemOrganizationSubscriptionGroup, ScheduleItemOrganizationClasspassGroup

"""
This helper file is added to allow function to add all subscription groups to a schedule item
ScheduleItem is already imported in the ScheduleItemOrganizationSubscriptionGroup model. 
Importing the SchedulItem model in ScheduleItemOrganizationSubscriptionGroup group generates an error.
"""


class ScheduleItemHelper:
    def add_all_subscription_groups(self, schedule_item_id):
        """
        Add all non-archived subscription groups to this schedule item
        """
        groups = OrganizationSubscriptionGroup.objects.filter(
            archived = False
        )

        for group in groups:
            schedule_item_subscription_group = ScheduleItemOrganizationSubscriptionGroup(
                schedule_item = ScheduleItem.objects.get(id=schedule_item_id),
                organization_subscription_group = group
            ).save()
            
    def add_all_classpass_groups(self, schedule_item_id):
        """
        Add all non-archived classpass groups to this schedule item
        """
        groups = OrganizationClasspassGroup.objects.filter(
            archived = False
        )

        for group in groups:
            schedule_item_classpass_group = ScheduleItemOrganizationClasspassGroup(
                schedule_item = ScheduleItem.objects.get(id=schedule_item_id),
                organization_classpass_group = group
            ).save()

    def schedule_item_with_otc_data(self, schedule_item, date):
        """
        Overwrite schedule_item object data with weekly otc data
        :param schedule_item: models.ScheduleItem object
        :param date: datetime.date
        :return:
        """
        if schedule_item.schedule_item_type == 'SPECIFIC':
            return schedule_item

        schedule_item_weekly_otc_qs = ScheduleItemWeeklyOTC.objects.filter(
            schedule_item=schedule_item,
            date=date
        )

        schedule_item_weekly_otc = None
        if schedule_item_weekly_otc_qs.exists():
            schedule_item_weekly_otc = schedule_item_weekly_otc_qs.first()

            # Change schedule item in memory before returning, but don't save it!
            if schedule_item_weekly_otc.account:
                schedule_item.account = schedule_item_weekly_otc.account
                schedule_item.role = schedule_item_weekly_otc.role
            if schedule_item_weekly_otc.account_2:
                schedule_item.account = schedule_item_weekly_otc.account_2
                schedule_item.role = schedule_item_weekly_otc.role_2
            if schedule_item_weekly_otc.organization_location_room:
                schedule_item.organization_location_room = schedule_item_weekly_otc.organization_location_room
            if schedule_item_weekly_otc.organization_classtype:
                schedule_item.organization_classtype = schedule_item_weekly_otc.organization_classtype
            if schedule_item_weekly_otc.organization_level:
                schedule_item.organization_level = schedule_item_weekly_otc.organization_level
            if schedule_item_weekly_otc.time_start:
                schedule_item.time_start = schedule_item_weekly_otc.time_start
            if schedule_item_weekly_otc.time_end:
                schedule_item.time_end = schedule_item_weekly_otc.time_end
                
        return schedule_item
