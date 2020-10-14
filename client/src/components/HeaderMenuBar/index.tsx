import React from 'react'
import { HeaderMenuBarContainer, OpenAsideMenuBarButton } from './styles'
import { RiMenuUnfoldLine } from 'react-icons/ri'

const HeaderMenuBar: React.FC = () => {
  return (
    <HeaderMenuBarContainer>
      <OpenAsideMenuBarButton>
        <RiMenuUnfoldLine />
      </OpenAsideMenuBarButton>

      <h1>Olá</h1>
    </HeaderMenuBarContainer>
  )
}

export default HeaderMenuBar
