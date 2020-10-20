import React from 'react'
import { HeaderMenuBarContainer, OpenAsideMenuBarButton } from './styles'
import { FiRadio } from 'react-icons/fi'

const HeaderMenuBar: React.FC = () => {
  return (
    <HeaderMenuBarContainer>
      <OpenAsideMenuBarButton>
        <FiRadio />
      </OpenAsideMenuBarButton>

      <span>Signal Reconstruction</span>
    </HeaderMenuBarContainer>
  )
}

export default HeaderMenuBar
