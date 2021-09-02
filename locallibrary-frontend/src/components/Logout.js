import React, {useContext} from 'react'
import axiosInstance from '../axios'
import {useHistory} from "react-router-dom"
import {AuthContext} from "../contexts/AuthContext"

function Logout() {
    const history = useHistory()

    const {LogoutFunction} = useContext(AuthContext)

    function handleClick(){
        axiosInstance.post("/catalog/api/logout",{refresh : localStorage.getItem("refresh_token")})
        .then((res) =>{
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            LogoutFunction()
            axiosInstance.defaults.headers['Authorization'] = null
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
