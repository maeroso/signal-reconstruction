import React, { useEffect, useState } from "react";
import { HeaderMenuBarContainer, OpenAsideMenuBarButton, MenuContainer, ActiveItem, Item, UserButton, UserMenu } from "./styles";
import { GiUltrasound } from "react-icons/gi";
import { RiLogoutBoxRLine } from 'react-icons/ri'
import { menu } from "./menu";
import { useUser } from "../../userContext";
import { useHistory } from "react-router-dom";

const HeaderMenuBar: React.FC = () => {
  const [menuItems, setMenuItems] = useState(menu);
  const { userName } = useUser()

  function handleMenuClick(clickedItem: any) {
    menuItems.map((item) => {
      if (item.name === clickedItem.name) {
        item.active = true;
      } else {
        item.active = false;
      }
    });

    setMenuItems([...menuItems]);
  }

  return (
    <HeaderMenuBarContainer>
      <OpenAsideMenuBarButton>
        <GiUltrasound style={{ fontSize: "40px" }} />
      </OpenAsideMenuBarButton>

      <span>Signal Reconstruction</span>

      <MenuContainer>
        {menuItems.map((item, i) => {
          if (item.active) {
            return (
              <ActiveItem
                title={item.name}
                onClick={() => handleMenuClick(item)}
                key={i}
              >
                <item.icon />
                <span style={{ marginLeft: '5px' }}>{ item.name }</span>
              </ActiveItem>
            );
          } else {
            return (
              <Item
                title={item.name}
                onClick={() => handleMenuClick(item)}
                key={i}
              >
                <item.icon />
                <span style={{ marginLeft: '5px' }}>{ item.name }</span>
              </Item>
            );
          }
        })}
      </MenuContainer>
      <UserButton>
        { userName }
      </UserButton>
      <UserMenu>
        <LogoutButton />
      </UserMenu>
    </HeaderMenuBarContainer>
  );
};

const LogoutButton: React.FC = () => {
  const { setIsLoggedIn } = useUser()
  const history = useHistory()

  const handleLogout = () => {
    history.push('/auth')
    localStorage.removeItem('user')
    setIsLoggedIn(false)
  }

  return (
    <button style={{
      backgroundColor: '#ed7b8a',
      color: 'white',
      borderTop: '1px solid darkred',
      position: 'absolute',
      bottom: 0,
      left: 0,
      right: -1,
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }} onClick={ handleLogout }>
      <RiLogoutBoxRLine style={{
        margin: '0 10px 0 0'
      }} />
      Logout
    </button>
  )
}

export default HeaderMenuBar;
