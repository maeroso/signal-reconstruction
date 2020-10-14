import styled from "styled-components";

export const HeaderMenuBarContainer = styled.header`
  width: 100vw;
  height: auto;
  max-height: 40px;

  background-color: #087f8c;

  display: flex;
  align-items: center;

  border-bottom: 2px;
  border-color: #076974;
`;

export const OpenAsideMenuBarButton = styled.button`
  background-color: #087f8c;
  height: 40px;
  width: 40px;

  border: none;

  transition: background-color 0.2s;

  :hover {
    background-color: #076974;
  }

  * {
    height: 60%;
    width: 60%;
  }
`;
