import React, {useState} from 'react'
import axiosInstance from '../axios'
import {useHistory} from "react-router-dom"
function Logout() {
    const history = useHistory()

    function handleClick(){
        axiosInstance.post("/catalog/api/logout",{refresh : localStorage.getItem("refresh_token")})
        .then((res) =>{
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user_id')
            localStorage.removeItem('isLibrarian')
            localStorage.removeItem('isLoggedIn')
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
