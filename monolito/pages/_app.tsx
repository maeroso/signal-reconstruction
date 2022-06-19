import '../styles/globals.css'
import type {AppProps} from 'next/app'
import HeaderMenuBar from "../components/HeaderMenuBar";
import React from "react";
import { ContentContainer } from '../components/Content/styles';

function MyApp({Component, pageProps}: AppProps) {
    return (
        <div>
            <HeaderMenuBar/>
            <ContentContainer>
                <Component {...pageProps} />
            </ContentContainer>
        </div>
    )
}

export default MyApp
