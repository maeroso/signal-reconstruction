import { createContext, useContext } from 'react';

interface UserContextType {
  userName: string,
  setUserName: (name: string) => void
  email: string,
  setEmail: (email: string) => void
  isLoggedIn: boolean,
  setIsLoggedIn: (isLoggedIn: boolean) => void,
  jobs: any,
  setJobs: (jobs: any) => void
}

export const UserContext = createContext<UserContextType>(
  { 
    userName: '', 
    setUserName: name => console.warn('no name provider'),
    email: '',
    setEmail: email => console.warn('no email provider'),
    isLoggedIn: false,
    setIsLoggedIn: isLoggedIn => console.warn('no user is logged provider'),
    jobs: [],
    setJobs: jobs => console.warn('no user is logged provider')
  }
);
export const useUser = () => useContext(UserContext);