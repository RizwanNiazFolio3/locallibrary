import React, {useState,useContext} from 'react'
import {GetToken} from "../../axios"
import {useHistory} from 'react-router-dom'
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
        GetToken(data,history,LoginFunction)
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
