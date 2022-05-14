import React, { useState } from 'react'
import { useHistory } from "react-router-dom";
import Card from '../../components/Card'
import axios from 'axios'

const AuthForm: React.FC = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isPswdConfirmed, setIsPswdConfirmed] = useState(false)
  
  const updateName = (evt: any) => {
    const name = evt.target.value;
    setName(name);
  }

  const updateEmail = (evt: any) => {
    const email = evt.target.value;
    setEmail(email);
  }

  const updatePassword = (evt: any) => {
    const pswd = evt.target.value;
    setPassword(pswd);
  }

  const updateConfirmPassword = (evt: any) => {
    const confirmPswd = evt.target.value;
    setConfirmPassword(confirmPswd);
    if (password === confirmPswd) {
      setIsPswdConfirmed(true)
    } else {
      setIsPswdConfirmed(false)
    }
  }

  return (
    <div className='center' style={{ flexDirection: 'column', margin: '10px 0' }}>
      <input type="text" placeholder='Nome' style={{ width: '70%' }} onChange={evt => updateName(evt)} />
      <input type="text" placeholder='E-mail' style={{ width: '70%' }} onChange={evt => updateEmail(evt)} />
      <input type="password" placeholder='Senha' style={{ width: '70%' }} onChange={evt => updatePassword(evt)} />
      <input type="password" placeholder='Confirmar senha' style={{ width: '70%' }} onChange={evt => updateConfirmPassword(evt)} />
      <div className="row" style={{ margin: '10px' }}>
        <RegisterButton name={name} email={email} password={password} isPswdConfirmed={isPswdConfirmed} />
      </div>
    </div>
  )
}

interface registerForm {
  name: string,
  email: string,
  password: string,
  isPswdConfirmed: boolean
}

const RegisterButton: React.FC<registerForm> = ({name, email, password, isPswdConfirmed}) => {
  const history = useHistory();

  const handleRegistration = (name: String, email: String, password: String, isPswdConfirmed: boolean) => {
    if (isPswdConfirmed) {
      axios.post('http://localhost:3333/auth/register', { name, email, password})
        .then((response) => {
          alert(response.data.message)
          if (response.status === 200) {
            history.push('/auth')
          }
        })
        .catch((err) => {
          console.error(err)
        })
    } else {
      alert('Senha não é igual a senha de confirmação!')
    }
  }

  return (
    <button type="button" onClick={ () => handleRegistration(name, email, password, isPswdConfirmed)}>
      Confirmar
    </button>
  );
}

const RegisterPage: React.FC = () => {
  return (
    <div className='center'>
      <Card title={'Registro'} Component={AuthForm} width={'80%'} />
    </div>
  )
}

export default RegisterPage
