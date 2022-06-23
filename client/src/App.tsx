import React, { useEffect, useState } from "react";
import Routes from "./routes";
import { GlobalStyle } from "./styles/GlobalStyle";
import "./styles/GlobalStyle.css";
import { UserContext } from "./userContext";

const App: React.FC = () => {
  const [userName, setUserName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [jobs, setJobs] = useState<any>([]);

  const checkUserIsLoggedIn = () => {
    const userStorage = localStorage.getItem('user')
    const userInfo = userStorage ? JSON.parse(atob(userStorage)) : {}

    setUserName(userInfo.name ? userInfo.name : '')
    setEmail(userInfo.email ? userInfo.email : '')
    setIsLoggedIn(userInfo.email ? true : false)
    setJobs([])
  }

  useEffect(() => {
    checkUserIsLoggedIn()
  }, [])

  return (
    <UserContext.Provider
      value={{
        userName,
        setUserName,
        email,
        setEmail,
        isLoggedIn,
        setIsLoggedIn,
        jobs,
        setJobs
      }}
    >
      <GlobalStyle />
      <Routes />
    </UserContext.Provider>
  );
};

export default App;
