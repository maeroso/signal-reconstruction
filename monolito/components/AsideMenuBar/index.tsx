import React, { useState } from 'react'

import { AsideMenuContainer, ActiveItem, Item } from './styles'
import { menu } from './menu'

const AsideMenuBar: React.FC = () => {
  const [ menuItems, setMenuItems ] = useState(menu)

  function handleMenuClick (clickedItem: any) {
    menuItems.map(item => {
      if (item.name === clickedItem.name) {
        item.active = true
      } else {
        item.active = false
      }
    })

    setMenuItems([...menuItems])
  }

  return (
    <AsideMenuContainer >
      {
        menuItems.map((item, i) => {
          if (item.active) {
            return (
              <ActiveItem title={item.name} onClick={() => handleMenuClick(item)} key={i} >
                <item.icon />
              </ActiveItem>
            )
          } else {
            return (
              <Item title={item.name} onClick={() => handleMenuClick(item)} key={i} >
                <item.icon />
              </Item>
            )
          }
        })
      }
    </AsideMenuContainer>
  )
}

export default AsideMenuBar
