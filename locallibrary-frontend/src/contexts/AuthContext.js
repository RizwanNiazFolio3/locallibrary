import React, { createContext, useState, useEffect } from 'react'
import jwt_decode from "jwt-decode";


export const AuthContext = createContext();



function AuthContextProvider({children}){
    /**
     * This context is where we store the state details as they pertain to the current user
     */
    const [isAuthenticated, setIsAuthenticated] = useState(false) //This is used for components that only render based on whether a user is logged in or not i.e the login/logout component
    const [user_id, setUser_Id] = useState(""); //This is used in case we need to use the current users id for any future api call or rendering i.e to check the books borrowed by the current user
    const [isLibrarian, setIsLibrarian] = useState(false) //This is used to render components based on whether or not the user has librarian credentials or not. a user can do create, update or delete operations


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

    //This function is called when a user successfully logs in
    const LoginFunction = (access_token) =>{
        setIsAuthenticated(true)
        setUser_Id(access_token.user_id)
        setIsLibrarian(access_token.isLibrarian)
    }

    //This is called when a user logs out
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
