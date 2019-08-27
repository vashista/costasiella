// @flow

import React from 'react'
import { v4 } from "uuid"
import { withTranslation } from 'react-i18next'


import {
  List
} from "tabler-react";
import HasPermissionWrapper from "../../../HasPermissionWrapper"

let attendance_active = false
let edit_active = false

function ClassMenu ({ t, scheduleItemId, class_date, active_link }) {
  switch (active_link) {
    case "attendance":
      attendance_active = true
      break
    case "edit":
      edit_active = true
      break
  }

  return (
    <List.Group transparent={true}>   
      <HasPermissionWrapper 
          resource="scheduleitemattendance"
          permission="view" 
      >
        <List.GroupItem
            key={v4()}
            className="d-flex align-items-center"
            to={"#/schedule/classes/class/attendance/" + scheduleItemId + "/" + class_date}
            icon="check-circle"
            active={attendance_active}
            >
            {t("general.attendance")}
        </List.GroupItem>
      </HasPermissionWrapper>
      <HasPermissionWrapper 
          resource="scheduleclassweeklyotc"
          permission="change" 
      >
        <List.GroupItem
            key={v4()}
            className="d-flex align-items-center"
            to={"#/schedule/classes/class/edit/" + scheduleItemId + "/" + class_date}
            icon="edit-3"
            active={edit_active}
            >
            {t("general.edit")}
        </List.GroupItem>
      </HasPermissionWrapper>

    </List.Group>
  )
}

export default withTranslation()(ClassMenu)