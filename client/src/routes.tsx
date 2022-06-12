import React, { useEffect, useState } from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import MainLayout from './layouts/Main'
import AuthLayout from './layouts/Auth'
import { useUser } from './userContext'

const Routes: React.FC = () => {
  const { isLoggedIn } = useUser();

  return (
    <BrowserRouter>
      <Switch>
        { isLoggedIn &&
          <Route path="/" component={MainLayout}></Route>
        }
        { !isLoggedIn && 
          <Route path="/" component={AuthLayout}></Route>
        }
      </Switch>
    </BrowserRouter>
  )
}

export default Routes
