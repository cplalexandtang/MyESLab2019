import React from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter } from 'react-router-dom'
import { Link, Switch, Route } from 'react-router-dom'
import Monitor from './containers/Monitor'
import Admin from './containers/Admin'


function App() {
  return (
    <BrowserRouter>
      <Link to="/monitor">Monitor</Link>
      <Link to="/admin">Admin</Link>
      <Switch>
        <Route path="/monitor" component={Monitor} />
        <Route path="/admin" component={Admin} />
      </Switch>
    </BrowserRouter>
  );
}

export default App;
