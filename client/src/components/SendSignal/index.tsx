import React from 'react'
import { Container, SendButton } from './styles'
import { FiUploadCloud } from 'react-icons/fi'

const SendSignal: React.FC = () => {
    return (
        <Container>
            <FiUploadCloud size={80} />
            <SendButton>Enviar</SendButton>
        </Container>
    )
}

export default SendSignal