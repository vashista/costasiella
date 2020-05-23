// @flow

import React, { Component, useState } from 'react'
import { useQuery, useMutation, useLazyQuery } from '@apollo/react-hooks'
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
  Table,
  StampCard
} from "tabler-react";
import { TimeStringToJSDateOBJ } from '../../../../tools/date_tools'
// import { confirmAlert } from 'react-confirm-alert'; // Import
import { toast } from 'react-toastify'


import ShopClassBookBack from "./ShopClassBookBack"
import ShopClassBookBase from "./ShopClassBookBase"
// import ScheduleClassBookClasspasses from "./ScheduleClassBookClasspasses"
// import ScheduleClassBookSubscriptions from "./ScheduleClassBookSubscriptions"
// import ScheduleClassBookPriceDropin from "./ScheduleClassBookPriceDropin"
// import ScheduleClassBookPriceTrial from "./ScheduleClassBookPriceTrial"
// import ClassEditBase from "../ClassEditBase"

import { GET_BOOKING_OPTIONS_QUERY } from "./queries"
// import CSLS from "../../../../../tools/cs_local_storage"


function ShopClassBook({ t, match, history }) {
  const schedule_item_id = match.params.class_id
  const class_date = match.params.date
  const { loading, error, data } = useQuery(
    GET_BOOKING_OPTIONS_QUERY, {
      variables: {
        scheduleItem: schedule_item_id,
        date: class_date,
        listType: "SHOP_BOOK"
      }
    }
  )

  // Loading
  if (loading) return (
    <ShopClassBookBase pageHeaderOptions={<ShopClassBookBack />}>
      <p>{t('general.loading_with_dots')}</p>
    </ShopClassBookBase>
  )
  // Error
  if (error) {
    console.log(error)
    return (
      <ShopClassBookBase pageHeaderOptions={<ShopClassBookBack />}>
        <p>{t('general.error_sad_smiley')}</p>
      </ShopClassBookBase>
    )
  }
  
  console.log(data)
  const account = data.scheduleClassBookingOptions.account
  const classpasses = data.scheduleClassBookingOptions.classpasses
  const subscriptions = data.scheduleClassBookingOptions.subscriptions
  const prices = data.scheduleClassBookingOptions.scheduleItemPrices
  const scheduleItem = data.scheduleClassBookingOptions.scheduleItem
  // const subtitle = class_subtitle({
  //   t: t,
  //   location: scheduleItem.organizationLocationRoom.organizationLocation.name, 
  //   locationRoom: scheduleItem.organizationLocationRoom.name,
  //   classtype: scheduleItem.organizationClasstype.name, 
  //   timeStart: TimeStringToJSDateOBJ(scheduleItem.timeStart), 
  //   date: class_date
  // })

  console.log(prices)
  
  
  return (
    <ShopClassBookBase pageHeaderOptions={<ShopClassBookBack />}>
      <Grid.Row>
        <Grid.Col md={12}>
          <h4>{t('general.booking_options')}</h4>
          <h5>Class info</h5>
          <div className="mt-6">
            <Grid.Row cards deck>
              {/* <ScheduleClassBookSubscriptions subscriptions={subscriptions} />
              <ScheduleClassBookClasspasses classpasses={classpasses} />
              {(prices) ?
                (prices.organizationClasspassDropin) ? 
                  <ScheduleClassBookPriceDropin priceDropin={prices.organizationClasspassDropin}/> : "" 
                : "" }
              {(prices) ?
                (prices.organizationClasspassTrial) ? 
                  <ScheduleClassBookPriceTrial priceTrial={prices.organizationClasspassTrial}/> : "" 
                : "" } */}
            </Grid.Row>
          </div>
        </Grid.Col>
      </Grid.Row>
    </ShopClassBookBase>
  )
}


export default withTranslation()(withRouter(ShopClassBook))

