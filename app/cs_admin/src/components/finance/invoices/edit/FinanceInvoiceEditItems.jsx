// @flow

import React from 'react'
import gql from "graphql-tag"
import { Query, Mutation } from "react-apollo"
import { useMutation } from '@apollo/react-hooks';
import { withTranslation } from 'react-i18next'
import { withRouter } from "react-router"
import { Formik } from 'formik'
import { toast } from 'react-toastify'
import { v4 } from 'uuid'


import {
  Card, 
  Table
} from "tabler-react"


import { get_list_query_variables } from "../tools"
import { UPDATE_INVOICE, GET_INVOICES_QUERY } from "../queries"
import UpdateProductName from "./UpdateProductName"
import UpdateDescription from "./UpdateDescription"
import UpdateQuantity from "./UpdateQuantity"
import UpdatePrice from "./UpdatePrice"
import UpdateFinanceTaxRate from "./UpdateFinanceTaxRate"
import FinanceInvoiceItemDelete from "./FinanceInvoiceItemDelete"
import FinanceInvoiceItemAdd from "./FinanceInvoiceItemAdd"


export const UPDATE_INVOICE_ITEM = gql`
  mutation UpdateFinanceInvoiceItem($input: UpdateFinanceInvoiceItemInput!) {
    updateFinanceInvoiceItem(input: $input) {
      financeInvoiceItem {
        id
        productName
        description
        quantity
        price
        financeTaxRate {
          id
          name
        }
      }
    }
  }
`


// function get_initial_values(node) {
//   let initialValues = {
//     productName: node.productName, 
//     description: node.description, 
//     quantity: node.quantity, 
//     price: node.price, 
//   }

//   if (node.financeTaxRate) {
//     initialValues.financeTaxRate = node.financeTaxRate.id
//   }

//   if (node.financeGlaccount) {
//     initialValues.financeGlaccount = node.financeGlaccount.id
//   }

//   if (node.financeCostcenter) {
//     initialValues.financeCostcenter = node.financeCostcenter.id
//   }

//   return initialValues

// }

{/* <Card.Options>
                  <Button color={(!archived) ? 'primary': 'secondary'}  
                          size="sm"
                          onClick={() => {archived=false; refetch({archived});}}>
                    {t('general.current')}
                  </Button>
                  <Button color={(archived) ? 'primary': 'secondary'} 
                          size="sm" 
                          className="ml-2" 
                          onClick={() => {archived=true; refetch({archived});}}>
                    {t('general.archive')}
                  </Button>
                </Card.Options> */}


const FinanceInvoiceEditItems = ({ t, history, match, refetchInvoice, inputData }) => (
  <Card statusColor="blue">
    <Card.Header>
      <Card.Title>{t('general.items')}</Card.Title>
      <Card.Options>
        <FinanceInvoiceItemAdd />
      </Card.Options>
    </Card.Header>
    <Card.Body>
      <Table>
        <Table.Header>
          <Table.Row>
            <Table.ColHeader>{t("general.product")}</Table.ColHeader>
            <Table.ColHeader>{t("general.description")}</Table.ColHeader>
            <Table.ColHeader>{t("general.quantity_short_and_price")}</Table.ColHeader>
            <Table.ColHeader>{t("general.tax")}</Table.ColHeader>
            <Table.ColHeader>{t("general.total")}</Table.ColHeader>
            <Table.ColHeader></Table.ColHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {inputData.financeInvoice.items.edges.map(({ node }) => (
            <Table.Row key={"item_" + node.id}>
              <Table.Col>
                <UpdateProductName initialValues={node} />
              </Table.Col>
              <Table.Col>
                <UpdateDescription initialValues={node} />
              </Table.Col>
              <Table.Col>
                <UpdateQuantity initialValues={node} />
                <UpdatePrice initialValues={node} />
              </Table.Col>
              <Table.Col>
                <UpdateFinanceTaxRate initialValues={node} inputData={inputData} />
              </Table.Col>
              <Table.Col>
                <span className="pull-right">{node.totalDisplay}</span>
              </Table.Col>
              <Table.Col>
                <FinanceInvoiceItemDelete node={node} />
              </Table.Col>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </Card.Body>
  </Card>
)

export default withTranslation()(withRouter(FinanceInvoiceEditItems))