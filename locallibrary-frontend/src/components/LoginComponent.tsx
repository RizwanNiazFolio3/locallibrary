import React, {useContext,useEffect,useState} from 'react'
import Logout from './Logout'
import {Link} from 'react-router-dom'
import {AuthContext} from '../contexts/AuthContext'


function LoginComponent() {
    //If the current user is authenticated, a logout button will be shown, otherwise,
    //A link to the login page will be rendered
    const {isAuthenticated}: {isAuthenticated: boolean} = useContext(AuthContext)
    const {LogoutFunction}: {LogoutFunction: () => void} = useContext(AuthContext)


//    useEffect(()=>{
//    },[])
    
    function isAuthenticatedIsTrue(){
        return(
            <>
            {console.log("LoginComponent is rendered with isAuthenticated = true")}
                <Logout />
            </>
        ) 
    }

    function isAuthenticatedIsFalse(){
        return(
            <>
            {console.log("LoginComponent is rendered with isAuthenticated = false")}
                <p><Link to = "/Login">Login</Link></p>
            </>
        )
    }
    return(
        <>
        {isAuthenticated === true? isAuthenticatedIsTrue():isAuthenticatedIsFalse()}
        </>
    )  
}

export default LoginComponent
