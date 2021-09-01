import React, {useState} from 'react'
import axiosInstance from "../../axios"
import {useHistory} from 'react-router-dom'
import jwt_decode from 'jwt-decode'

function Login() {
    const history = useHistory()
    const [userName, setUserName] = useState("")
    const [password, setPassword] = useState("")

    function handleSubmit(event){
        event.preventDefault();
        console.log(userName)
        console.log(password)
        const data = {
            username: userName,
            password: password
        }
        axiosInstance.post("/catalog/api/token/",data)
        .then((res) =>{
            localStorage.setItem('access_token',res.data.access)
            localStorage.setItem('refresh_token',res.data.refresh)
            const decoded_token = jwt_decode(localStorage.getItem("access_token"))
            localStorage.setItem('user_id',decoded_token.user_id)
            localStorage.setItem('isLibrarian',decoded_token.isLibrarian)
            localStorage.setItem('isLoggedIn',true)
            console.log(localStorage.getItem("isLibrarian"))
            console.log(localStorage.getItem('user_id'))
            axiosInstance.defaults.headers['Authorization'] = "Bearer " + localStorage.getItem('access_token')
            history.push('/')
        })
    }

    return (
        <div>
            <form onSubmit = {handleSubmit}>
                <label>
                    User Name
                    <input 
                        type="text" 
                        value={userName}
                        placeholder="Username"
                        onChange={(e)=>setUserName(e.target.value.trim())}
                    />
                </label>
                <br/>
                <label>
                    Password
                    <input
                        type="password"
                        value={password}
                        onChange={(e)=>setPassword(e.target.value)}
                    />
                </label>
                <br/>
                <button>Login</button>
            </form>
        </div>
    )
}

export default Login
