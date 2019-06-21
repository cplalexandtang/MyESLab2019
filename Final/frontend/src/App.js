import React, { Component } from 'react';
import './App.css';
import { BrowserRouter } from 'react-router-dom'
import { Link, Switch, Route } from 'react-router-dom'
import Monitor from './containers/Monitor'
import Admin from './containers/Admin'
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink
} from 'reactstrap';


class App extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false
    };
  }

  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  

  render() {
    return (
      <BrowserRouter>
        <Navbar color="light" light expand="md">
          <NavbarBrand href="/">MD305</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="ml-auto" navbar>
              <NavItem>
                <NavLink tag={Link} href="/monitor" to="/monitor/">Monitor</NavLink>
              </NavItem>
              <NavItem>
                <NavLink tag={Link} href="/Admin" to="/Admin/">Admin</NavLink>
              </NavItem>
            </Nav>
          </Collapse>
        </Navbar>
        <Switch>
          <Route path="/monitor" component={Monitor} />
          <Route path="/admin" component={Admin} />
        </Switch>
      </BrowserRouter>
    );

  }
}

export default App;
