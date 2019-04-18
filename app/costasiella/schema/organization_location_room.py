from django.utils.translation import gettext as _

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from ..models import OrganizationLocation, OrganizationLocationRoom
from ..modules.gql_tools import require_login_and_permission, get_rid
from ..modules.messages import Messages

m = Messages()

class OrganizationLocationRoomNode(DjangoObjectType):
    class Meta:
        model = OrganizationLocationRoom
        filter_fields = ['archived']
        interfaces = (graphene.relay.Node, )

    @classmethod
    def get_node(self, info, id):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.view_organizationlocationroom')

        # Return only public non-archived location rooms
        return self._meta.model.objects.get(id=id)


class OrganizationLocationRoomQuery(graphene.ObjectType):
    organization_location_rooms = DjangoFilterConnectionField(OrganizationLocationRoomNode)
    organization_location_room = graphene.relay.Node.Field(OrganizationLocationRoomNode)

    def resolve_organization_locations(self, info, id, archived=False, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception(m.user_not_logged_in)
        # if not info.context.user.is_authenticated:
            # return OrganizationLocation.objects.none()
        # else:
            # return OrganizationLocation.objects.all()
        ## return everything:
        if user.has_perm('costasiella.view_organizationlocationroom'):
            return OrganizationLocationRoom.objects.filter(organization_location=id, archived = archived).order_by('name')

        # Return only public non-archived locations
        return OrganizationLocation.objects.filter(organization_location=id, display_public = True, archived = False).order_by('name')


class CreateOrganizationLocationRoom(graphene.relay.ClientIDMutation):
    class Input:
        organization_location = graphene.ID(required=True)
        name = graphene.String(required=True)
        display_public = graphene.Boolean(required=True)

    organization_location_room = graphene.Field(OrganizationLocationRoomNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, **input):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.add_organizationlocationroom')

        if not len(input['name']):
            raise GraphQLError(_('Name is required'))

        rid = get_rid(input['organization_location'])
        organization_location = OrganizationLocation.objects.filter(id=rid.id).first()
        if not organization_location:
            raise Exception('Invalid Organization Location ID!')

        organization_location_room = OrganizationLocationRoom(
            organization_location = organization_location,
            name=input['name'], 
            display_public=input['display_public']
        )
        organization_location_room.save()

        return CreateOrganizationLocationRoom(organization_location_room=organization_location_room)


class UpdateOrganizationLocationRoom(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        display_public = graphene.Boolean(required=True)
        
    organization_location_room = graphene.Field(OrganizationLocationRoomNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, **input):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.change_organizationlocationroom')

        rid = get_rid(input['id'])

        organization_location_room = OrganizationLocationRoom.objects.filter(id=rid.id).first()
        if not organization_location_room:
            raise Exception('Invalid Organization Location Room ID!')

        organization_location_room.name = input['name']
        organization_location_room.display_public = input['display_public']
        organization_location_room.save(force_update=True)

        return UpdateOrganizationLocationRoom(organization_location_room=organization_location_room)


class ArchiveOrganizationLocationRoom(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        archived = graphene.Boolean(required=True)

    organization_location_room = graphene.Field(OrganizationLocationRoomNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, **input):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.delete_organizationlocationroom')

        rid = get_rid(input['id'])

        organization_location_room = OrganizationLocationRoom.objects.filter(id=rid.id).first()
        if not organization_location_room:
            raise Exception('Invalid Organization Location Room ID!')

        organization_location_room.archived = input['archived']
        organization_location_room.save(force_update=True)

        return ArchiveOrganizationLocationRoom(organization_location_room=organization_location_room)


class OrganizationLocationRoomMutation(graphene.ObjectType):
    archive_organization_location_room = ArchiveOrganizationLocationRoom.Field()
    create_organization_location_room = CreateOrganizationLocationRoom.Field()
    update_organization_location_room = UpdateOrganizationLocationRoom.Field()
    