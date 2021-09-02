import React, {useContext} from 'react'
import Logout from './Logout'
import {Link} from 'react-router-dom'
import {AuthContext} from '../contexts/AuthContext'


function LoginComponent() {
    const {isAuthenticated} = useContext(AuthContext)
    if (isAuthenticated === true){
        return(
            <>
                <Logout />
            </>
        ) 
    }
    else{
        return(
            <>
                <p><Link to = "/Login">Login</Link></p>
            </>
        )  
    }
}

export default LoginComponent
