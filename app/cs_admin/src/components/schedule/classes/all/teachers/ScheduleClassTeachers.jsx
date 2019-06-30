// @flow

import React from 'react'
import { Query, Mutation } from "react-apollo"
import gql from "graphql-tag"
import { v4 } from "uuid"
import { withTranslation } from 'react-i18next'
import { withRouter } from "react-router"
import { Link } from 'react-router-dom'
import moment from 'moment'

import {
  Alert,
  Page,
  Grid,
  Icon,
  Dimmer,
  Badge,
  Button,
  Card,
  Container,
  Table
} from "tabler-react";
import SiteWrapper from "../../../../SiteWrapper"
import HasPermissionWrapper from "../../../../HasPermissionWrapper"
import { TimeStringToJSDateOBJ } from '../../../../../tools/date_tools'
// import { confirmAlert } from 'react-confirm-alert'; // Import
import { toast } from 'react-toastify'
import { class_edit_all_subtitle, represent_teacher_role } from "../tools"
import confirm_delete from "../../../../../tools/confirm_delete"

import ContentCard from "../../../../general/ContentCard"
import ClassEditBase from "../ClassEditBase"

import { GET_SCHEDULE_CLASS_TEACHERS_QUERY } from "./queries"

const DELETE_SCHEDULE_CLASS_TEACHER = gql`
  mutation DeleteScheduleClassTeacher($input: DeleteScheduleItemTeacherInput!) {
    deleteScheduleItemTeacher(input: $input) {
      ok
    }
  }
`

const ScheduleClassTeachers = ({ t, history, match }) => (
  <SiteWrapper>
    <div className="my-3 my-md-5">
      {console.log('ID here:')}
      {console.log(match.params.class_id)}
      <Query query={GET_SCHEDULE_CLASS_TEACHERS_QUERY} variables={{ scheduleItem: match.params.class_id }}>
        {({ loading, error, data, refetch, fetchMore }) => {
          // Loading
          if (loading) return (
            <ClassEditBase menu_active_link="teachers">
              <Dimmer active={true} loader={true} />
            </ClassEditBase>
          )
          // Error
          if (error) return (
            <ClassEditBase menu_active_link="teachers">
              <p>{t('schedule.classes.teachers.error_loading')}</p>
            </ClassEditBase>
          )
          // const headerOptions = <Card.Options>
          //   <Button color={(!archived) ? 'primary': 'secondary'}  
          //           size="sm"
          //           onClick={() => {archived=false; refetch({archived});}}>
          //     {t('general.current')}
          //   </Button>
          //   <Button color={(archived) ? 'primary': 'secondary'} 
          //           size="sm" 
          //           className="ml-2" 
          //           onClick={() => {archived=true; refetch({archived});}}>
          //     {t('general.archive')}
          //   </Button>
          // </Card.Options>

          const initialTimeStart = TimeStringToJSDateOBJ(data.scheduleItem.timeStart)
          const subtitle = class_edit_all_subtitle({
            t: t,
            location: data.scheduleItem.organizationLocationRoom.organizationLocation.name,
            locationRoom: data.scheduleItem.organizationLocationRoom.name,
            classtype: data.scheduleItem.organizationClasstype.name,
            starttime: initialTimeStart
          })

          // Empty list
          if (!data.scheduleItemTeachers.edges.length) { return (
            <ClassEditBase menu_active_link="teachers" subtitle={subtitle}>
              <p>{t('schedule.classes.teachers.empty_list')}</p>
            </ClassEditBase>
          )} else {   
          // Life's good! :)
            return (
              <ClassEditBase menu_active_link="teachers" default_card={false} subtitle={subtitle}>
              <ContentCard 
                cardTitle={t('schedule.classes.title_edit')}
                // headerContent={headerOptions}
                pageInfo={data.scheduleItemTeachers.pageInfo}
                onLoadMore={() => {
                fetchMore({
                  variables: {
                    after: data.scheduleItemTeachers.pageInfo.endCursor
                  },
                  updateQuery: (previousResult, { fetchMoreResult }) => {
                    const newEdges = fetchMoreResult.scheduleItemTeachers.edges
                    const pageInfo = fetchMoreResult.scheduleItemTeachers.pageInfo

                    return newEdges.length
                      ? {
                          // Put the new locations at the end of the list and update `pageInfo`
                          // so we have the new `endCursor` and `hasNextPage` values
                          data: { 
                            scheduleItemTeachers: {
                              __typename: previousResult.scheduleItemTeachers.__typename,
                              edges: [ ...previousResult.scheduleItemTeachers.edges, ...newEdges ],
                              pageInfo
                            }
                          }
                        }
                      : previousResult
                    }
                  })
                }} >
                <div>
                  <Table>
                    <Table.Header>
                      <Table.ColHeader>{t('general.date_start')}</Table.ColHeader>
                      <Table.ColHeader>{t('general.date_end')}</Table.ColHeader>
                      <Table.ColHeader>{t('general.teacher')}</Table.ColHeader>
                      <Table.ColHeader>{t('general.teacher_2')}</Table.ColHeader>
                      <Table.ColHeader></Table.ColHeader>
                      <Table.ColHeader></Table.ColHeader>
                    </Table.Header>
                    <Table.Body>
                      {data.scheduleItemTeachers.edges.map(({ node }) => (
                        <Table.Row key={v4()}>
                          <Table.Col key={v4()}> 
                            {moment(node.dateStart).format('LL')}
                          </Table.Col>
                          <Table.Col key={v4()}> 
                            {(node.dateEnd) ? moment(node.dateEtart).format('LL') : ""}
                          </Table.Col>
                          <Table.Col>
                            {node.account.fullName} <br />
                            {represent_teacher_role(node.role)}
                          </Table.Col>
                          <Table.Col>
                            {node.account2 ?
                              <span>
                                {node.account2.fullName} <br />
                                {represent_teacher_role(node.role2)}
                              </span> : ""
                            }
                          </Table.Col>
                          <Table.Col className="text-right" key={v4()}>
                            <Button className='btn-sm' 
                                    onClick={() => history.push("/schedule/classes/all/teachers/" + match.params.class_id + '/edit/' + node.id)}
                                    color="secondary">
                              {t('general.edit')}
                            </Button>
                          </Table.Col>
                          <Mutation mutation={DELETE_SCHEDULE_CLASS_TEACHER} key={v4()}>
                            {(deleteScheduleItemTeacher, { data }) => (
                              <Table.Col className="text-right" key={v4()}>
                                <button className="icon btn btn-link btn-sm" 
                                    title={t('general.delete')} 
                                    href=""
                                    onClick={() => {
                                      confirm_delete({
                                        t: t,
                                        msgConfirm: t('schedule.classes.teachers.delete_confirm_msg'),
                                        msgDescription: <p>{t('schedule.classes.teachers.delete_confirm_description')}</p>,
                                        msgSuccess: t('schedule.classes.,teachers.deleted'),
                                        deleteFunction: deleteScheduleItemTeacher,
                                        functionVariables: { variables: {
                                          input: {
                                            id: node.id
                                          }
                                        }, refetchQueries: [
                                          {query: GET_SCHEDULE_CLASS_TEACHERS_QUERY, variables: { scheduleItem: match.params.class_id }}
                                        ]}
                                    })}}
                                >
                                  <span className="text-red">
                                    <Icon prefix="fe" name="trash-2" />
                                  </span>
                                </button>
                              </Table.Col>
                            )}
                          </Mutation>
                        </Table.Row>
                      ))}
                    </Table.Body>
                  </Table>

                  {/* <Table>
                    <Table.Header>
                      <Table.Row key={v4()}>
                        <Table.ColHeader>{t('general.name')}</Table.ColHeader>
                        <Table.ColHeader>{t('general.public')}</Table.ColHeader>
                      </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {location_rooms.edges.map(({ node }) => (
                          <Table.Row key={v4()}>
                            <Table.Col key={v4()}>
                              {node.name}
                            </Table.Col>
                            <Table.Col key={v4()}>
                              {(node.displayPublic) ? 
                                <Badge color="success">{t('general.yes')}</Badge>: 
                                <Badge color="danger">{t('general.no')}</Badge>}
                            </Table.Col>
                            <Table.Col className="text-right" key={v4()}>
                              {(node.archived) ? 
                                <span className='text-muted'>{t('general.unarchive_to_edit')}</span> :
                                <Button className='btn-sm' 
                                        onClick={() => history.push("/organization/locations/rooms/edit/" + match.params.location_id + '/' + node.id)}
                                        color="secondary">
                                  {t('general.edit')}
                                </Button>
                              }
                            </Table.Col>
                            <Mutation mutation={ARCHIVE_LOCATION_ROOM} key={v4()}>
                              {(archiveLocationsRoom, { data }) => (
                                <Table.Col className="text-right" key={v4()}>
                                  <button className="icon btn btn-link btn-sm" 
                                      title={t('general.archive')} 
                                      href=""
                                      onClick={() => {
                                        console.log("clicked archived")
                                        let id = node.id
                                        archiveLocationsRoom({ variables: {
                                          input: {
                                          id,
                                          archived: !archived
                                          }
                                  }, refetchQueries: [
                                      { 
                                        query: GET_LOCATION_ROOMS_QUERY, 
                                        variables: {"archived": archived, organizationLocation: match.params.location_id }
                                      }
                                  ]}).then(({ data }) => {
                                    console.log('got data', data);
                                    toast.success(
                                      (archived) ? t('general.unarchived'): t('general.archived'), {
                                        position: toast.POSITION.BOTTOM_RIGHT
                                      })
                                  }).catch((error) => {
                                    toast.error((t('general.toast_server_error')) + ': ' +  error, {
                                        position: toast.POSITION.BOTTOM_RIGHT
                                      })
                                    console.log('there was an error sending the query', error);
                                  })
                                  }}>
                                    <Icon prefix="fa" name="inbox" />
                                  </button>
                                </Table.Col>
                              )}
                            </Mutation>
                          </Table.Row>
                        ))}
                    </Table.Body>
                  </Table> */}
                  </div>
                </ContentCard>
              </ClassEditBase>
          )}}
        }
      </Query>
    </div>
  </SiteWrapper>
);

export default withTranslation()(withRouter(ScheduleClassTeachers))