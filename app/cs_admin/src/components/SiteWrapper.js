// @flow

import * as React from "react"
import { NavLink, withRouter } from "react-router-dom"
import { Query } from "react-apollo"
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'
import 'react-confirm-alert/src/react-confirm-alert.css'

import GET_USER from "../queries/system/get_user"

import {
  Site,
  Nav,
  Grid,
  List,
  Button,
  RouterContextProvider,
} from "tabler-react";

import type { NotificationProps } from "tabler-react";

type Props = {|
  +children: React.Node,
|};

type State = {|
  notificationsObjects: Array<NotificationProps>,
|};

type subNavItem = {|
  +value: string,
  +to?: string,
  +icon?: string,
  +LinkComponent?: React.ElementType,
|};

type navItem = {|
  +value: string,
  +to?: string,
  +icon?: string,
  +active?: boolean,
  +LinkComponent?: React.ElementType,
  +subItems?: Array<subNavItem>,
  +useExact?: boolean,
|};

const navBarItems: Array<navItem> = [
  {
    value: "Home",
    to: "/",
    icon: "home",
    LinkComponent: withRouter(NavLink),
    useExact: true,
  },
  // {
  //   value: "Interface",
  //   icon: "box",
  //   subItems: [
  //     {
  //       value: "Cards Design",
  //       to: "/cards",
  //       LinkComponent: withRouter(NavLink),
  //     },
  //     { value: "Charts", to: "/charts", LinkComponent: withRouter(NavLink) },
  //     {
  //       value: "Pricing Cards",
  //       to: "/pricing-cards",
  //       LinkComponent: withRouter(NavLink),
  //     },
  //   ],
  // },
  // {
  //   value: "Components",
  //   icon: "calendar",
  //   subItems: [
  //     { value: "Maps", to: "/maps", LinkComponent: withRouter(NavLink) },
  //     { value: "Icons", to: "/icons", LinkComponent: withRouter(NavLink) },
  //     { value: "Store", to: "/store", LinkComponent: withRouter(NavLink) },
  //     { value: "Blog", to: "/blog", LinkComponent: withRouter(NavLink) },
  //   ],
  // },
  // {
  //   value: "Pages",
  //   icon: "file",
  //   subItems: [
  //     { value: "Profile", to: "/profile", LinkComponent: withRouter(NavLink) },
  //     { value: "Login", to: "/login", LinkComponent: withRouter(NavLink) },
  //     {
  //       value: "Register",
  //       to: "/register",
  //       LinkComponent: withRouter(NavLink),
  //     },
  //     {
  //       value: "Forgot password",
  //       to: "/forgot-password",
  //       LinkComponent: withRouter(NavLink),
  //     },
  //     { value: "400 error", to: "/400", LinkComponent: withRouter(NavLink) },
  //     { value: "401 error", to: "/401", LinkComponent: withRouter(NavLink) },
  //     { value: "403 error", to: "/403", LinkComponent: withRouter(NavLink) },
  //     { value: "404 error", to: "/404", LinkComponent: withRouter(NavLink) },
  //     { value: "500 error", to: "/500", LinkComponent: withRouter(NavLink) },
  //     { value: "503 error", to: "/503", LinkComponent: withRouter(NavLink) },
  //     { value: "Email", to: "/email", LinkComponent: withRouter(NavLink) },
  //     {
  //       value: "Empty page",
  //       to: "/empty-page",
  //       LinkComponent: withRouter(NavLink),
  //     },
  //     { value: "RTL", to: "/rtl", LinkComponent: withRouter(NavLink) },
  //   ],
  // },
  {
    value: "School",
    to: "/school",
    icon: "book",
    LinkComponent: withRouter(NavLink),
  },
];

// const accountDropdownProps = 


// const GET_USER = gql`
//   query {
//     user {
//     id
//     isActive
//     email
//     firstName
//     lastName
//     userPermissions {
//       id
//     }
//     groups {
//       id
//       name
//       permissions {
//         id
//         name
//         codename
//       }
//     }
//   }
//   }
// `

class SiteWrapper extends React.Component<Props, State> {
  state = {}  

  render(): React.Node {
    return (
      <Query query={GET_USER} >
        {({ loading, error, data }) => {
          if (loading) return <p>Loading...</p>;
          if (error) return <p>Error loading user... :(</p>; 
          
          
          console.log('user data in site wrapper')
          console.log(data)
      

          return <Site.Wrapper
            headerProps={{
                href: "/",
                alt: "Costasiella",
                imageURL: "/static/logo_stock_backend.svg", // Set logo url here
                navItems: (
                  <Nav.Item type="div" className="d-none d-md-flex">
                    <Button
                      icon="settings"
                      href="https://github.com/tabler/tabler-react"
                      target="_blank"
                      outline
                      size="sm"
                      RootComponent="a"
                      color="primary"
                    >
                      Settings
                    </Button>
                  </Nav.Item>
                ),
                // notificationsTray: {
                //   notificationsObjects,
                //   markAllAsRead: () =>
                //     this.setState(
                //       () => ({
                //         notificationsObjects: this.state.notificationsObjects.map(
                //           v => ({ ...v, unread: false })
                //         ),
                //       }),
                //       () =>
                //         setTimeout(
                //           () =>
                //             this.setState({
                //               notificationsObjects: this.state.notificationsObjects.map(
                //                 v => ({ ...v, unread: true })
                //               ),
                //             }),
                //           5000
                //         )
                //     ),
                //   unread: unreadCount,
                // },
                accountDropdown: {
                avatarURL: "",
                name: data.user.firstName + ' ' + data.user.lastName,
                description: "",
                options: [
                  // { icon: "user", value: "Profile" },
                  { icon: "lock", value: "Change password", to: "/accounts/password/change/" },
                  { isDivider: true },
                  { icon: "log-out", value: "Sign out", to: "/accounts/logout/" },
                ],
              },
              }}
              navProps={{ itemsObjects: navBarItems }}
              routerContextComponentType={withRouter(RouterContextProvider)}
              footerProps={{
                // links: [
                //   <a href="#">First Link</a>,
                //   <a href="#">Second Link</a>,
                //   <a href="#">Third Link</a>,
                //   <a href="#">Fourth Link</a>,
                //   <a href="#">Five Link</a>,
                //   <a href="#">Sixth Link</a>,
                //   <a href="#">Seventh Link</a>,
                //   <a href="#">Eigth Link</a>,
                // ],
                // note:
                //   "Premium and Open Source dashboard template with responsive and high quality UI. For Free!",
                copyright: (
                  <React.Fragment>
                    Copyright © 2019.
                    <a
                      href="https://www.costasiella.com"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {" "}
                      Edwin van de Ven.
                    </a>{" "}
                    All rights reserved.
                  </React.Fragment>
                ),
                nav: (
                  <React.Fragment>
                    <Grid.Col auto={true}>
                      {/* <List className="list-inline list-inline-dots mb-0">
                        <List.Item className="list-inline-item">
                          <a href="./docs/index.html">Documentation</a>
                        </List.Item>
                        <List.Item className="list-inline-item">
                          <a href="./faq.html">FAQ</a>
                        </List.Item>
                      </List> */}
                    </Grid.Col>
                    <Grid.Col auto={true}>
                      {/* <Button
                        href="https://github.com/tabler/tabler-react"
                        size="sm"
                        outline
                        color="primary"
                        RootComponent="a"
                      >
                        Source code
                      </Button> */}
                    </Grid.Col>
                  </React.Fragment>
                ),
              }}
            >
              {this.props.children}
              <ToastContainer autoClose={5000}/>
            </Site.Wrapper>
          }}
        </Query>
    );
  }
}

export default SiteWrapper;