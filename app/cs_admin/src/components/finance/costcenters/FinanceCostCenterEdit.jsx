// @flow

import React, {Component } from 'react'
import gql from "graphql-tag"
import { Query, Mutation } from "react-apollo";
import { withTranslation } from 'react-i18next'
import { withRouter } from "react-router"
import { Formik, Form as FoForm, Field, ErrorMessage } from 'formik'
import { toast } from 'react-toastify'

import { GET_COSTCENTERS_QUERY, GET_COSTCENTER_QUERY } from './queries'
import { COSTCENTER_SCHEMA } from './yupSchema'



import {
  Page,
  Grid,
  Icon,
  Button,
  Card,
  Container,
  Form
} from "tabler-react";
import SiteWrapper from "../../SiteWrapper"
import HasPermissionWrapper from "../../HasPermissionWrapper"

import FinanceMenu from "../FinanceMenu"


const UPDATE_COSTCENTER = gql`
  mutation UpdateFinanceCostCenter($input: UpdateFinanceCostCenterInput!) {
    updateFinanceCostcenter(input: $input) {
      financeCostcenter {
        id
        name
        code
      }
    }
  }
`


class FinanceCostCenterEdit extends Component {
  constructor(props) {
    super(props)
    console.log("finance costcenter edit props:")
    console.log(props)
  }

  render() {
    const t = this.props.t
    const match = this.props.match
    const history = this.props.history
    const id = match.params.id
    const return_url = "/finance/costcenters"

    return (
      <SiteWrapper>
        <div className="my-3 my-md-5">
          <Container>
            <Page.Header title={t('finance.costcenters.title')} />
            <Grid.Row>
              <Grid.Col md={9}>
              <Card>
                <Card.Header>
                  <Card.Title>{t('finance.costcenters.title_edit')}</Card.Title>
                  {console.log(match.params.id)}
                </Card.Header>
                <Query query={GET_COSTCENTER_QUERY} variables={{ id }} >
                {({ loading, error, data, refetch }) => {
                    // Loading
                    if (loading) return <p>{t('loading_with_dots')}</p>
                    // Error
                    if (error) {
                      console.log(error)
                    return <p>{t('error_sad_smiley')}</p>
                    }
                    
                    const initialData = data.financeCostcenter;
                    console.log('query data')
                    console.log(data)

                    return (
                      
                      <Mutation mutation={UPDATE_COSTCENTER} onCompleted={() => history.push(return_url)}> 
                      {(updateGlaccount, { data }) => (
                          <Formik
                              initialValues={{ 
                                name: initialData.name, 
                                code: initialData.code
                              }}
                              validationSchema={COSTCENTER_SCHEMA}
                              onSubmit={(values, { setSubmitting }) => {
                                  console.log('submit values:')
                                  console.log(values)

                                  updateGlaccount({ variables: {
                                    input: {
                                      id: match.params.id,
                                      name: values.name,
                                      code: values.code
                                    }
                                  }, refetchQueries: [
                                      {query: GET_COSTCENTERS_QUERY, variables: {"archived": false }}
                                  ]})
                                  .then(({ data }) => {
                                      console.log('got data', data)
                                      toast.success((t('finance.costcenters.toast_edit_success')), {
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
                              {({ isSubmitting, errors, values }) => (
                                  <FoForm>
                                      <Card.Body>
                                        <Form.Group label={t('name')}>
                                          <Field type="text" 
                                                  name="name" 
                                                  className={(errors.name) ? "form-control is-invalid" : "form-control"} 
                                                  autoComplete="off" />
                                          <ErrorMessage name="name" component="span" className="invalid-feedback" />
                                        </Form.Group>
                                        <Form.Group label={t('finance.costcenters.code')}>
                                          <Field type="text" 
                                                  name="code" 
                                                  className={(errors.code) ? "form-control is-invalid" : "form-control"} 
                                                  autoComplete="off" />
                                          <ErrorMessage name="code" component="span" className="invalid-feedback" />
                                        </Form.Group>
                                      </Card.Body>
                                      <Card.Footer>
                                          <Button 
                                            className="pull-right"
                                            color="primary"
                                            disabled={isSubmitting}
                                            type="submit"
                                          >
                                            {t('submit')}
                                          </Button>
                                          <Button
                                            type="button" 
                                            color="link" 
                                            onClick={() => history.push(return_url)}
                                          >
                                              {t('cancel')}
                                          </Button>
                                      </Card.Footer>
                                  </FoForm>
                              )}
                          </Formik>
                      )}
                      </Mutation>
                      )}}
                </Query>
              </Card>
              </Grid.Col>
              <Grid.Col md={3}>
                <HasPermissionWrapper permission="change"
                                      resource="financecostcenter">
                  <Button color="primary btn-block mb-6"
                          onClick={() => history.push(return_url)}>
                    <Icon prefix="fe" name="chevrons-left" /> {t('back')}
                  </Button>
                </HasPermissionWrapper>
                <FinanceMenu active_link='costcenters'/>
              </Grid.Col>
            </Grid.Row>
          </Container>
        </div>
    </SiteWrapper>
    )}
  }


export default withTranslation()(withRouter(FinanceCostCenterEdit))