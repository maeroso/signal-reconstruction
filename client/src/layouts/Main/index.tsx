import React from 'react'
import AsideMenuBar from '../../components/AsideMenuBar'
import HeaderMenuBar from '../../components/HeaderMenuBar'
import { ContentContainer } from '../../components/Content/styles'
import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom'
import FunctionalPage from '../../pages/FunctionalPage'
import HomePage from '../../pages/HomePage'

const MainLayout: React.FC = () => {
  return (
    <div>
      <HeaderMenuBar />
      <ContentContainer>
        <BrowserRouter>
          <Switch>
            <Route path="/home" component={HomePage}></Route>
            <Route path="/archives" component={FunctionalPage}></Route>
            <Redirect from='/' to='/home'/>
          </Switch>
        </BrowserRouter>
      </ContentContainer>
    </div>
  )
}

export default MainLayout