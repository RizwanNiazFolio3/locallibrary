import React, { createContext, useState, useEffect } from 'react'
import jwt_decode from "jwt-decode";


export const AuthContext = createContext();

function AuthContextProvider({children}){
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [user_id, setUser_Id] = useState("");
    const [isLibrarian, setIsLibrarian] = useState(false)

    useEffect(() =>{
        if (localStorage.getItem('access_token') != null){
            setIsAuthenticated(true)
            setUser_Id(jwt_decode(localStorage.getItem('access_token')).user_id)
            setIsLibrarian(jwt_decode(localStorage.getItem('access_token')).isLibrarian)
        }
        else{
            setIsAuthenticated(false)
            setUser_Id("")
            setIsLibrarian(false)
        }
    },[])

    const LoginFunction = (access_token) =>{
        setIsAuthenticated(true)
        setUser_Id(access_token.user_id)
        setIsLibrarian(access_token.isLibrarian)
    }

    const LogoutFunction = () =>{
        setIsAuthenticated(false)
        setUser_Id("")
        setIsLibrarian(false)
    }

    return (
        <AuthContext.Provider value={{
                isAuthenticated, 
                user_id, 
                isLibrarian, 
                LoginFunction:LoginFunction, 
                LogoutFunction:LogoutFunction
            }
        }>
            {children}
        </AuthContext.Provider>
    )

}

export default AuthContextProvider
