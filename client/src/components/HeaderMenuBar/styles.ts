import styled from "styled-components";

export const HeaderMenuBarContainer = styled.header`
  position: relative;
  width: 100vw;
  height: 30px;
  max-height: 30px;

  font-weight: 800;
  font-size: 12px;

  background: #94ce;

  display: flex;
  align-items: center;

  border-bottom: 2px;
  border-color: #076974;
`;

export const OpenAsideMenuBarButton = styled.button`
  background-color: transparent;
  font-size: 50px;
  margin-bottom: 10px;

  color: #fff;

  border: none;

  transition: background-color 0.2s;

  * {
    height: 60%;
    width: 60%;
  }
`;

export const MenuContainer = styled.section`
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;

  align-items: center;

  margin-left: 40px;
`

export const ActiveItem = styled.div`
  background-color: rgba(196, 196, 196, 0.5);
  padding: 10px;
  cursor: pointer;
  margin: 0 5px 10px 5px;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 500;
`

export const Item = styled.div`
  padding: 10px;
  cursor: pointer;
  margin-bottom: 10px;
  font-size: 13px;
  font-weight: 400;
`;

export const UserButton = styled.button`
  position: absolute;
  right: 10px;
  background: transparent;
  height: 30px;
  font-size: 12px;
`

export const UserMenu = styled.div`
  position: absolute;
  top: 35px;
  right: 10px;
  background: #fff;
  width: 270px;
  height: 150px;
  border-radius: 2px;
  box-shadow: 1px 1px 1px rgba(55, 55, 55, 0.5);
`