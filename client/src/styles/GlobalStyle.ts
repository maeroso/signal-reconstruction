import { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background-color: #0f0f05;
        font-size: 14px;
        color: #fff;
        font-family: 'Ubuntu', sans-serif;      
    }
`;
