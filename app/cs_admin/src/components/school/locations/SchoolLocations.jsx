import React from 'react'
import { Query } from "react-apollo"
import gql from "graphql-tag"
import { v4 } from "uuid"


// @flow

import {
  Page,
  Grid,
  Badge,
  Button,
  Card,
  Container,
  List,
  Form,
  Table
} from "tabler-react";
import SiteWrapper from "../../SiteWrapper"
import HasPermissionWrapper from "../../HasPermissionWrapper"

import SchoolMenu from "../SchoolMenu"

const GET_LOCATIONS = gql`
  {
    schoolLocations {
        id
        name
    }
  }
`


const SchoolLocations = () => (
  <SiteWrapper>
    <div className="my-3 my-md-5">
      <Container>
        <Grid.Row>
          <Grid.Col md={3}>
            <h3 className="page-title mb-5">School</h3>
            <SchoolMenu active_link='schoollocation'/>
          </Grid.Col>
          <Grid.Col md={9}>
          <Card>
            <Card.Header>
              <Card.Title>Locations</Card.Title>
              <HasPermissionWrapper permission="add"
                                    resource="schoollocation">
                Add something                      
              </HasPermissionWrapper>
            </Card.Header>
            <Card.Body>
              <Query query={GET_LOCATIONS}>
                {({ loading, error, data }) => {
                  if (loading) return <p>Loading...</p>
                  if (error) return <p>Error loading school locations :(</p>
                  if (!data.schoolLocations) {
                    return "No locations found."
                  } else {
                    return (
                      <Table>
                        <Table.Header>
                          <Table.Row key={v4()}>
                            <Table.ColHeader>Name</Table.ColHeader>
                          </Table.Row>
                        </Table.Header>
                        <Table.Body>
                           {data.schoolLocations.map(({ id, name }) => (
                              <Table.Row key={v4()}>
                                <Table.Col key={v4()}>
                                  {name}
                                </Table.Col>
                              </Table.Row>
                            ))}
                        </Table.Body>
                      </Table>
                    )
                  }
                }}
              </Query>
            </Card.Body>
          </Card>
          </Grid.Col>
        </Grid.Row>
      </Container>
    </div>
  </SiteWrapper>
);

export default SchoolLocations