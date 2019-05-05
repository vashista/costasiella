from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Q

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ..modules.gql_tools import require_login_and_permission, get_rid


class AccountNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = ['trashed']
        interfaces = (graphene.relay.Node, )

    @classmethod
    def get_node(self, info, id):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.view_account')
        #TODO: Add permission for accounts to get their own info or all info with view permission

        return self._meta.model.objects.get(id=id)


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission


class CreateAccount(graphene.Mutation):
    user = graphene.Field(AccountNode)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    # def mutate(self, info, username, password, email):
    def mutate(self, info, password, email):
        user = get_user_model()(
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateAccount(user=user)


class AccountMutation(graphene.ObjectType):
    create_user = CreateAccount.Field()


class AccountQuery(graphene.AbstractType):
    # account = graphene.Field(AccountNode)
    account = graphene.relay.Node.Field(AccountNode)
    accounts = DjangoFilterConnectionField(AccountNode)
    # group = graphene.List(GroupType, search=graphene.String())
    # permission = graphene.List(PermissionType)

    def resolve_account(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

    def resolve_accounts(self, info, trashed=False, **kwargs):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.view_account')

        return get_user_model().objects.filter(trashed=trashed).order_by('first_name')

    def resolve_group(self, info, search=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        if search:
            filter = (
                Q(name__icontains=search)
            )
            return Groups.objects.filter(filter)

        return Group.objects.all()


    def resolve_permission(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Permission.objects.all()
        # user = info.context.user
        # if user.is_anonymous:
        #     raise Exception('Not logged in!')
        # if user:
        #     return Permission.objects.filter(user=user)

        
