import React, {useState,useContext} from 'react'
import {client} from "../../axios"
import {useHistory} from 'react-router-dom'
import jwt_decode from 'jwt-decode'
import { AuthContext, DecodedToken } from '../../contexts/AuthContext'
import {UserLoginData} from '../../CustomTypes'





function Login() {
    /**
     * When the users credentials are authenticated, the refresh token and access token are stored in localstorage.
     * The details of the user are stored in state with the help of the useContext hook
     */
    const {LoginFunction}: {LoginFunction: (arg0: DecodedToken) => void} = useContext(AuthContext)

    const history = useHistory()
    const [userName, setUserName]: [string, React.Dispatch<React.SetStateAction<string>>] = useState("")
    const [password, setPassword]: [string, React.Dispatch<React.SetStateAction<string>>] = useState("")

    function handleSubmit(event: React.FormEvent<HTMLFormElement>){
        event.preventDefault();
        const data:UserLoginData = {
            username: userName,
            password: password
        }
        client.Login(data)
        .then(Token =>{
            localStorage.setItem('access_token',Token.access_token)
            localStorage.setItem('refresh_token',Token.refresh_token)
            const tok: string | null = localStorage.getItem("access_token");
            console.log(tok)
            if(tok){
                console.log('came here')
                const decoded_token: DecodedToken = jwt_decode(tok)
                //passing the decoded access token to the AuthContext to get the state variables needed to render for the
                //current user
                LoginFunction(decoded_token)
                client.SetAxiosHeaders("Bearer " + localStorage.getItem('access_token'))
                history.push('/')
            }
        })


        // })
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
