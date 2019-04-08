// @flow

import React, {Component } from 'react'
import { withTranslation } from 'react-i18next'
import { withRouter } from "react-router"

import {
  Page,
  Grid,
  Icon,
  Button,
  Card,
  Container,
  StampCard
} from "tabler-react";
import SiteWrapper from "../../SiteWrapper"
import HasPermissionWrapper from "../../HasPermissionWrapper"

import SchoolMenu from "../SchoolMenu"


class SchoolHome extends Component {
  constructor(props) {
    super(props)
    console.log("School home props:")
    console.log(props)
  }


  render() {
    const t = this.props.t
    const match = this.props.match
    const history = this.props.history
    const id = match.params.id

    return (
      <SiteWrapper>
        <div className="my-3 my-md-5">
          <Container>
            <Page.Header title={t("school.page_header")} />
            <Grid.Row>
              <Grid.Col md={9}>
                <Grid.Row>
                  <Grid.Col md={4} lg={4}>
                    <div onClick={() => history.push('/school/locations')}>
                      <StampCard header={<small>{t('school.locations.title')}</small>} footer={t('')} color="blue" icon="home" />
                    </div>
                  </Grid.Col>
                  <Grid.Col md={4} lg={4}>
                    <div onClick={() => history.push('/school/classtypes')}>
                      <StampCard header={<small>{t('school.classtypes.title')}</small>} footer={t('')} color="blue" icon="book-open" />
                    </div>
                  </Grid.Col>
                  <Grid.Col md={4} lg={4}>
                    <div onClick={() => history.push('/school/discoveries')}>
                      <StampCard header={<small>{t('school.discoveries.title')}</small>} footer={t('')} color="blue" icon="compass" />
                    </div>
                  </Grid.Col>
                  <Grid.Col md={4} lg={4}>
                    <div onClick={() => history.push('/school/memberships')}>
                      <StampCard header={<small>{t('school.memberships.title')}</small>} footer={t('')} color="blue" icon="clipboard" />
                    </div>
                  </Grid.Col>
                </Grid.Row>
              </Grid.Col>
              <Grid.Col md={3}>
                <SchoolMenu />
              </Grid.Col>
            </Grid.Row>
          </Container>
        </div>
    </SiteWrapper>
    )}
  }


export default withTranslation()(withRouter(SchoolHome))