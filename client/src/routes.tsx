import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import MainLayout from './layouts/Main'

const Routes: React.FC = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" component={MainLayout}></Route>
      </Switch>
    </BrowserRouter>
  )
}

export default Routes
