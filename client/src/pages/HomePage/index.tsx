import React from 'react'
import Card from '../../components/Card'
import SendSignal from '../../components/SendSignal'
import JobsTable from '../../components/JobsTable'

const HomePage: React.FC = () => {
  return (
    <div>
      <Card title={'Enviar Sinal'} Component={SendSignal} width={'100%'} />
      <JobsTable />
    </div>
  )
}

export default HomePage
