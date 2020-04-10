from django.utils.translation import gettext as _

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from ..models import Account, FinanceOrder, OrganizationClasspass
from ..modules.gql_tools import require_login_and_permission, get_rid
from ..modules.messages import Messages
from ..modules.finance_tools import display_float_as_amount

m = Messages()

class FinanceOrderInterface(graphene.Interface):
    id = graphene.GlobalID()
    order_number = graphene.Int()
    subtotal_display = graphene.String()
    tax_display = graphene.String()
    total_display = graphene.String()
    paid_display = graphene.String()
    balance_display = graphene.String()


class FinanceOrderNode(DjangoObjectType):
    class Meta:
        model = FinanceOrder
        filter_fields = {
            'account': ['exact'],
            'status': ['exact'],
        }
        interfaces = (graphene.relay.Node, FinanceOrderInterface, )

    def resolve_order_number(self, info):
        return self.id

    def resolve_subtotal_display(self, info):
        return display_float_as_amount(self.subtotal)

    def resolve_tax_display(self, info):
        return display_float_as_amount(self.tax)

    def resolve_total_display(self, info):
        return display_float_as_amount(self.total)


    @classmethod
    def get_node(self, info, id):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.view_financeorder')

        return self._meta.model.objects.get(id=id)


class FinanceOrderQuery(graphene.ObjectType):
    finance_orders = DjangoFilterConnectionField(FinanceOrderNode)
    finance_order = graphene.relay.Node.Field(FinanceOrderNode)

    def resolve_finance_orders(self, info, archived=False, **kwargs):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.view_financeorder')

        return FinanceOrder.objects.all().order_by('-pk')


def validate_create_update_input(input, update=False):
    """
    Validate input
    """ 
    result = {}

    # Fetch & check organization classpass
    if 'organization_classpass' in input:
        rid = get_rid(input["organization_classpass"])
        organization_classpass = OrganizationClasspass.objects.get(id=rid.id)
        result['organization_classpass'] = organization_classpass
        if not organization_classpass:
            raise Exception(_('Invalid Organization Classpass ID!'))

    return result


class CreateFinanceOrder(graphene.relay.ClientIDMutation):
    class Input:
        note = graphene.String(required=False, default_value="")
        organization_classpass = graphene.ID(required=False)
        
    finance_order = graphene.Field(FinanceOrderNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, **input):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.add_financeorder')

        validation_result = validate_create_update_input(input)

        finance_order = FinanceOrder(
            account = user,
        )

        if 'note' in input:
            finance_order.note = input['note']

        # Save order
        finance_order.save()

        # Process items
        if 'organization_classpass' in validation_result:
            #TODO: actually add item
            finance_order.item_add_classpass(validation_result['organization_classpass'])
        

        return CreateFinanceOrder(finance_order=finance_order)


class UpdateFinanceOrder(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        status = graphene.String(required=False)
        note = graphene.String(required=False)

    finance_order = graphene.Field(FinanceOrderNode)

    @classmethod
    def mutate_and_get_payload(self, root, info, **input):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.change_financeinvoice')

        print(input)
        rid = get_rid(input['id'])

        finance_order = FinanceOrder.objects.filter(id=rid.id).first()
        if not finance_order:
            raise Exception('Invalid Finance Order ID!')

        if 'status' in input:
            # TODO: Validate status input
            finance_order.status = input['status']

        if 'note' in input:
            finance_order.note = input['note']

        finance_order.save()

        return UpdateFinanceOrder(finance_order=finance_order)


class DeleteFinanceOrder(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    
    @classmethod
    def mutate_and_get_payload(self, root, info, **input):
        user = info.context.user
        require_login_and_permission(user, 'costasiella.delete_financeorder')

        rid = get_rid(input['id'])

        finance_order = FinanceOrder.objects.filter(id=rid.id).first()
        if not finance_order:
            raise Exception('Invalid Finance Order ID!')

        ok = finance_order.delete()

        return DeleteFinanceOrder(ok=ok)


class FinanceOrderMutation(graphene.ObjectType):
    delete_finance_order = DeleteFinanceOrder.Field()
    create_finance_order = CreateFinanceOrder.Field()
    update_finance_order = UpdateFinanceOrder.Field()