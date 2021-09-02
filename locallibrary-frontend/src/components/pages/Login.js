import React, {useState,useContext} from 'react'
import axiosInstance from "../../axios"
import {useHistory} from 'react-router-dom'
import jwt_decode from 'jwt-decode'
import { AuthContext } from '../../contexts/AuthContext'

function Login() {
    /**
     * When the users credentials are authenticated, the refresh token and access token are stored in localstorage.
     * The details of the user are stored in state with the help of the useContext hook
     */
    const {LoginFunction} = useContext(AuthContext)

    const history = useHistory()
    const [userName, setUserName] = useState("")
    const [password, setPassword] = useState("")

    function handleSubmit(event){
        event.preventDefault();
        const data = {
            username: userName,
            password: password
        }
        axiosInstance.post("/catalog/api/token/",data)
        .then((res) =>{
            //Storing the access and refresh tokens.
            localStorage.setItem('access_token',res.data.access)
            localStorage.setItem('refresh_token',res.data.refresh)
            //passing the decoded access token to the AuthContext to get the state variables needed to render for the
            //current user
            const decoded_token = jwt_decode(localStorage.getItem("access_token"))
            LoginFunction(decoded_token)
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
