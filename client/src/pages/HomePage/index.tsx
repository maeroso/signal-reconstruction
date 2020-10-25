import React from 'react'
import Card from '../../components/Card'
import LastImages from '../../components/LastImages'
import SendSignal from '../../components/SendSignal'

const HomePage: React.FC = () => {
  return (
    <div>
      <Card title={'Últimas Imagens'} Component={LastImages} width={'100%'} />
      <Card title={'Enviar Sinal'} Component={SendSignal} width={'100%'} />
    </div>
  )
}

export default HomePage
