import React, {useState, useEffect} from 'react'
import Logout from './Logout'
import {Link} from 'react-router-dom'


function LoginComponent() {

    if (localStorage.getItem("isLoggedIn") == "true"){
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
