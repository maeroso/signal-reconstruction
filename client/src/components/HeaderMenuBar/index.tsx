import React, { useEffect, useState } from "react";
import { HeaderMenuBarContainer, OpenAsideMenuBarButton, MenuContainer, ActiveItem, Item, UserButton, UserMenu } from "./styles";
import { GiUltrasound } from "react-icons/gi";
import { RiLogoutBoxRLine } from 'react-icons/ri'
import { menu } from "./menu";
import { useUser } from "../../userContext";
import { useHistory } from "react-router-dom";

const HeaderMenuBar: React.FC = () => {
  const [menuItems, setMenuItems] = useState(menu);
  const { userName, email } = useUser()
  const [userMenuState, setUserMenuState] = useState<boolean>(false)

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

  const handleUserMenuOpening = () => {
    setUserMenuState(!userMenuState)
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
      <UserButton onClick={ handleUserMenuOpening }>
        { userName }
      </UserButton>
      { userMenuState && 
        <UserMenu>
          <span style={{ color: '#333', margin: '5px' }}>
            E-mail: { email }
          </span>
          <LogoutButton />
        </UserMenu>
      }
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
      backgroundColor: '#ffff',
      color: 'red',
      borderTop: '1px solid #e1e1e1',
      position: 'absolute',
      bottom: 0,
      left: -2,
      right: -2,
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
