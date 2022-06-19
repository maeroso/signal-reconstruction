import React, { CSSProperties } from 'react'
import { CardContainer } from './styles'

interface CardContent {
    title: String;
    Component: React.FC<any>;
    width?: CSSProperties['width'];
}

const Card: React.FC<CardContent> = ({ title, Component, width }) => {
    if (!width) {
        width = 'max-content'
    }
    
    return(
      <CardContainer style={{ width }}>
          <h3>{ title }</h3>
          <Component />
      </CardContainer>
    )
}

export default Card