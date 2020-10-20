import styled from 'styled-components'

export const AsideMenuContainer = styled.section`
  position: absolute;
  left: 0;
  top: 40px;
  bottom: 0;

  background: linear-gradient(180deg, rgba(34, 188, 151, 0.62) 0%, rgba(34, 188, 151, 0) 100%);

  width: 50px;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;

  align-items: center;

  font-size: 25px;
`

export const ActiveItem = styled.div`
  background-color: rgba(196, 196, 196, 0.5);
  padding: 8px;
  cursor: pointer;
  margin: 0 5px 10px 5px;
  border-radius: 5px
`

export const Item = styled.div`
  padding: 10px;
  cursor: pointer;
  margin-bottom: 10px;
`