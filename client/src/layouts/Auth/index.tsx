import React from 'react'
import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom'
import AuthPage from '../../pages/AuthPage'
import RegisterPage from '../../pages/RegisterPage'

const MainLayout: React.FC = () => {
  return (
    <div>
      <BrowserRouter>
        <Switch>
          <Route path="/auth" component={AuthPage}></Route>
          <Route path="/register" component={RegisterPage}></Route>
          <Redirect from='/' to='/auth'/>
        </Switch>
      </BrowserRouter>
    </div>
  )
}

export default MainLayout