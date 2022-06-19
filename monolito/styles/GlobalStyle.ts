import { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    background-color: #f9f9f9;
    font-size: 14px;
    color: #fff;
    font-family: 'Ubuntu', sans-serif;      
  }

  input {
    padding: 10px;
    outline: none;
  }

  .row {
    display: flex;
    flex-direction: row;
  }

  .center {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  button {
    padding: 10px;
    color: #fff;
    margin: 0 2px;
    background-color: #076974;
    border: none;
    cursor: pointer;
  }
`;
