import gql from "graphql-tag"

export const GET_SUBSCRIPTION_GROUPS_QUERY = gql`
  query OrganizationSubscriptionGroups($after: String, $before: String, $archived: Boolean) {
    organizationSubscriptionGroups(first: 15, before: $before, after: $after, archived: $archived) {
      pageInfo {
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
      }
      edges {
        node {
          id
          archived
          name
        }
      }
    }
  }
`


export const GET_SUBSCRIPTION_GROUP_QUERY = gql`
  query OrganizationSubscriptionGroup($id: ID!) {
    organizationSubscriptionGroup(id:$id) {
      id
      name
      archived
    }
  }
`


export const GET_SUBSCRIPTION_GROUP_PASSES_QUERY = gql`
  query GetPassesAndGroupMembership($after: String, $before: String, $archived: Boolean, $id:ID!) {
    organizationSubscriptions(first: 15, before: $before, after: $after, archived: $archived) {
      pageInfo {
        startCursor
        endCursor
        hasNextPage
        hasPreviousPage
      }
      edges {
        node {
          id
          name
        }
      }
    }
    organizationSubscriptionGroup(id: $id) {
      id
      name
      organizationSubscriptions {
        edges {
          node {
            id
            name
          }
        }
      }
    }
  }
`