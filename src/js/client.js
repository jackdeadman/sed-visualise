import React from 'react';
import ReactDom from 'react-dom';

import Main from './layouts/Main';
import Play from './pages/Play';
import Index from './pages/Index';

import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router';

const app = document.getElementById('app');

ReactDom.render(
  <Router history={browserHistory}>
    <Route path="/" component={Main}>
        <IndexRoute component={Index} />
        <Route path="play/:code" component={Play} />
    </Route>
  </Router>
  , app);
