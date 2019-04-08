// @flow

import React from 'react'
import { Mutation } from "react-apollo";
import gql from "graphql-tag"
import { withTranslation } from 'react-i18next'
import { withRouter } from "react-router"
import { Formik, Form as FoForm, Field, ErrorMessage } from 'formik'
import { toast } from 'react-toastify'


import { GET_DISCOVERIES_QUERY } from './queries'
import { DISCOVERY_SCHEMA } from './yupSchema'


import {
  Page,
  Grid,
  Icon,
  Button,
  Card,
  Container,
  Form,
} from "tabler-react"
import SiteWrapper from "../../SiteWrapper"
import HasPermissionWrapper from "../../HasPermissionWrapper"

import SchoolMenu from '../SchoolMenu'


const ADD_DISCOVERY = gql`
  mutation CreateSchoolDiscovery($input:CreateSchoolDiscoveryInput!) {
    createSchoolDiscovery(input: $input) {
      schoolDiscovery{
        id
        archived
        name
      }
    }
  }
`

const return_url = "/school/discoveries"

const SchoolDiscoveryAdd = ({ t, history }) => (
  <SiteWrapper>
    <div className="my-3 my-md-5">
      <Container>
        <Page.Header title={t('school.page_title')} />
        <Grid.Row>
          <Grid.Col md={9}>
          <Card>
            <Card.Header>
              <Card.Title>{t('school.discoveries.title_add')}</Card.Title>
            </Card.Header>
            <Mutation mutation={ADD_DISCOVERY} onCompleted={() => history.push(return_url)}> 
                {(addLocation, { data }) => (
                    <Formik
                        initialValues={{ name: '', code: '' }}
                        validationSchema={DISCOVERY_SCHEMA}
                        onSubmit={(values, { setSubmitting }) => {
                            addLocation({ variables: {
                              input: {
                                name: values.name, 
                              }
                            }, refetchQueries: [
                                {query: GET_DISCOVERIES_QUERY, variables: {"archived": false }}
                            ]})
                            .then(({ data }) => {
                                console.log('got data', data);
                                toast.success((t('school.discoveries.toast_add_success')), {
                                    position: toast.POSITION.BOTTOM_RIGHT
                                  })
                              }).catch((error) => {
                                toast.error((t('toast_server_error')) + ': ' +  error, {
                                    position: toast.POSITION.BOTTOM_RIGHT
                                  })
                                console.log('there was an error sending the query', error)
                                setSubmitting(false)
                              })
                        }}
                        >
                        {({ isSubmitting, errors }) => (
                            <FoForm>
                                <Card.Body>
                                    <Form.Group label={t('name')}>
                                      <Field type="text" 
                                              name="name" 
                                              className={(errors.name) ? "form-control is-invalid" : "form-control"} 
                                              autoComplete="off" />
                                      <ErrorMessage name="name" component="span" className="invalid-feedback" />
                                    </Form.Group>
                                </Card.Body>
                                <Card.Footer>
                                    <Button 
                                      color="primary"
                                      className="pull-right" 
                                      type="submit" 
                                      disabled={isSubmitting}
                                    >
                                      {t('submit')}
                                    </Button>
                                    <Button color="link" onClick={() => history.push(return_url)}>
                                        {t('cancel')}
                                    </Button>
                                </Card.Footer>
                            </FoForm>
                        )}
                    </Formik>
                )}
                </Mutation>
          </Card>
          </Grid.Col>
          <Grid.Col md={3}>
            <HasPermissionWrapper permission="add"
                                  resource="schooldiscovery">
              <Button color="primary btn-block mb-6"
                      onClick={() => history.push(return_url)}>
                <Icon prefix="fe" name="chevrons-left" /> {t('back')}
              </Button>
            </HasPermissionWrapper>
            <SchoolMenu active_link='schooldiscoveries'/>
          </Grid.Col>
        </Grid.Row>
      </Container>
    </div>
  </SiteWrapper>
)

export default withTranslation()(withRouter(SchoolDiscoveryAdd))