import styled from 'styled-components'

export const Container = styled.div`
    display:flex;
    flex-direction: column;
    
    align-items: center;
    justify-content: center; 
`

export const Row = styled.div`
    display: flex;
    flex-direction: row;

    align-items: center;
    justify-content: center;
`

export const SendButton = styled.button`
    border: none;
    background: #95cf;
    border-radius: 5px;
    color: #fff;
    padding: 10px;
    cursor: pointer;
    margin: 40px 0;
`

export const SearchButton = styled.button`
    border: none;
    background: #fff;
    border-radius: 5px;
    color: #95cf;
    padding: 10px;
    cursor: pointer;
    margin: 40px 0;
`