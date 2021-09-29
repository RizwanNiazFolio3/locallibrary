import React, {useContext} from 'react'
import {client} from '../axios'
import {useHistory} from "react-router-dom"
import {AuthContext} from "../contexts/AuthContext"

function Logout() {
    const history = useHistory()

    const {LogoutFunction}: {LogoutFunction: () => void} = useContext(AuthContext)

    //Upon logout, the access tokens and refresh tokens are deleted and the current refresh token is added to
    //A blacklist to prevent it from being used
    function handleClick(){
        //The logout api endpoint takes the current refresh token and adds it to the blacklist
        client.Logout()
        .then(res=>{
            //Access and refresh tokens removed from localStorage
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            //The state variables in the context provider are set to default
            LogoutFunction()
            //The authorization in the headers is set to null for all future requests
            client.SetAxiosHeaders(null)
            history.push('/')
        })
    }

    return (
        <>
            <button onClick={handleClick}>Logout</button>   
        </>
    )
}

export default Logout
