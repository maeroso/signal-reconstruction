import styled from "styled-components";

export const HeaderMenuBarContainer = styled.header`
  width: 100vw;
  height: 40px;
  max-height: 40px;

  font-weight: 300;
  font-size: 20px;

  background: linear-gradient(90deg, rgba(34, 188, 151, 0.62) 19.62%, rgba(34, 188, 151, 0) 80.38%);

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
