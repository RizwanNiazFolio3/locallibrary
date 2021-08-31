import React, {useState} from 'react'
import axiosInstance from "../../axios"
import jwt_decode from "jwt-decode";
import {useHistory} from 'react-router-dom'

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
        axiosInstance.post("catalog/api/token/",data)
        .then((res) =>{
            localStorage.setItem('access_token',res.data.access)
            localStorage.setItem('refresh_token',res.data.refresh)
            console.log(localStorage.getItem('access_token'))
            console.log(localStorage.getItem('refresh_token'))
            console.log(jwt_decode(localStorage.getItem('access_token')))
            console.log(jwt_decode(localStorage.getItem('refresh_token')))
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
