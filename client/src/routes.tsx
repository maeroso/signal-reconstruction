import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import MainPage from './pages/MainPage/index'

const Routes: React.FC = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" component={MainPage}></Route>
      </Switch>
    </BrowserRouter>
  )
}

export default Routes
