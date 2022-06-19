import axios from "axios";
import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import Card from "../../components/Card";
import { useUser } from '../../userContext'

const AuthForm: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const updateEmail = (evt: any) => {
    const email = evt.target.value;
    setEmail(email);
  }

  const updatePassword = (evt: any) => {
    const pswd = evt.target.value;
    setPassword(pswd);
  }

  return (
    <div
      className="center"
      style={{ flexDirection: "column", margin: "10px 0" }}
    >
      <input type="text" placeholder="E-mail" style={{ width: "70%" }} onChange={evt => updateEmail(evt)} />
      <input type="password" placeholder="Senha" style={{ width: "70%" }} onChange={evt => updatePassword(evt)} />
      <div className="row" style={{ margin: "10px" }}>
        <LoginButton email={ email } password={ password } />
        <RegisterButton />
      </div>
    </div>
  );
};

interface LoginForm {
  email: string,
  password: string
}

const LoginButton: React.FC<LoginForm> = ({ email, password }) => {
  const history = useHistory();
  const { setUserName, setEmail, setIsLoggedIn } = useUser()

  const handleLogin = (email: string, password: string) => {
    if (email !== '' && password != '') {
      axios.post('http://localhost:3333/auth/login', { email, password })
        .then((response) => {
          if (response.status === 200) {
            alert(response.data.message)
            localStorage.setItem('user', btoa(JSON.stringify({
              name: response.data.name,
              email: response.data.email
            })))
            history.push('/')
            //useEffect(() => {
              setUserName(response.data.name)
              setEmail(response.data.email)
              setIsLoggedIn(true)
            //}, [])
          }
        })
        .catch((err) => {
          console.error(err)
        })
    } else {
      alert('Preencha os campos')
    }
    history.push('/')
  };

  return (
    <button onClick={() => handleLogin(email, password)}>Entrar</button>
  );
};

const RegisterButton: React.FC = () => {
  const history = useHistory();

  const handleGoToRegister = () => {
    history.push('/register')
  };

  return (
    <button
      style={{ backgroundColor: "transparent", color: "#076974" }}
      onClick={handleGoToRegister}
    >
      Registrar-se
    </button>
  );
};

const AuthPage: React.FC = () => {
  return (
    <div className="center">
      <Card title={"Autenticação"} Component={AuthForm} width={"80%"} />
    </div>
  );
};

export default AuthPage;
