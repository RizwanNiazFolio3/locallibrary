import React, {useContext} from 'react'
import Logout from './Logout'
import {Link} from 'react-router-dom'
import {AuthContext} from '../contexts/AuthContext'


function LoginComponent() {
    //If the current user is authenticated, a logout button will be shown, otherwise,
    //A link to the login page will be rendered
    const {isAuthenticated}: {isAuthenticated: boolean} = useContext(AuthContext)

    function isAuthenticatedIsTrue(){
        return(
            <>
                <Logout />
            </>
        ) 
    }

    function isAuthenticatedIsFalse(){
        return(
            <>
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
