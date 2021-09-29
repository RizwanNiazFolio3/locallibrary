import React, {useContext} from 'react'
import {Axioslogout} from '../axios'
import {useHistory} from "react-router-dom"
import {AuthContext} from "../contexts/AuthContext"

function Logout() {
    const history = useHistory()

    const {LogoutFunction}: {LogoutFunction: () => void} = useContext(AuthContext)

    //Upon logout, the access tokens and refresh tokens are deleted and the current refresh token is added to
    //A blacklist to prevent it from being used
    function handleClick(){
        Axioslogout(history,LogoutFunction)
    }

    return (
        <>
            <button onClick={handleClick}>Logout</button>   
        </>
    )
}

export default Logout
