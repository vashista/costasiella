import graphene
import graphql_jwt

from .financecostcenter import FinanceCostCenterQuery, FinanceCostCenterMutation
from .financeglaccount import FinanceGLAccountQuery, FinanceGLAccountMutation
from .financetaxrate import FinanceTaxRateQuery, FinanceTaxRateMutation

from .schoolclasscard import SchoolClasscardQuery, SchoolClasscardMutation
from .schoolclasstype import SchoolClasstypeQuery, SchoolClasstypeMutation
from .schooldiscovery import SchoolDiscoveryQuery, SchoolDiscoveryMutation
from .schoollocation import SchoolLocationQuery, SchoolLocationMutation
from .schoolmembership import SchoolMembershipQuery, SchoolMembershipMutation
from .user import UserQuery, UserMutation


class Query(FinanceCostCenterQuery,
            FinanceGLAccountQuery,
            FinanceTaxRateQuery,
            SchoolClasscardQuery,
            SchoolClasstypeQuery,
            SchoolDiscoveryQuery,
            SchoolLocationQuery, 
            SchoolMembershipQuery,
            UserQuery, 
            graphene.ObjectType):
    node = graphene.relay.Node.Field()


class Mutation(FinanceCostCenterMutation,
               FinanceGLAccountMutation,
               FinanceTaxRateMutation,
               SchoolClasscardMutation,
               SchoolClasstypeMutation,
               SchoolDiscoveryMutation,
               SchoolLocationMutation,
               SchoolMembershipMutation, 
               UserMutation, 
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

