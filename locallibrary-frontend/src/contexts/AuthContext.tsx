import React, { createContext, useState, useEffect } from 'react'
import jwt_decode from "jwt-decode";


// The attributes of decoded token
export type DecodedToken = {
    user_id: number;
    isLibrarian: boolean;
    isAuthenticated: boolean;
}

export interface DecodedRefreshToken {
    token_type:string,
    exp:number,
    jti:string,
    user_id:number,
    isLibrarian:boolean
}

// The attributes in context
type ContextAttributes = {
    user_id: number;
    isLibrarian: boolean;
    isAuthenticated: boolean;
    LoginFunction: (arg0: DecodedToken) => void;
    LogoutFunction: () => void;
}



const default_value: DecodedToken = {user_id: -1, isLibrarian: false, isAuthenticated: false};

export const AuthContext = createContext<ContextAttributes>({
    ...default_value,
    LoginFunction: (default_value: DecodedToken) => {},
    LogoutFunction: () => {}
});



function AuthContextProvider({children}: {children: JSX.Element[]}){
    /**
     * This context is where we store the state details as they pertain to the current user
     */
    const [isAuthenticated, setIsAuthenticated]: [boolean , React.Dispatch<React.SetStateAction<boolean>>] = useState<boolean>(false); //This is used for components that only render based on whether a user is logged in or not i.e the login/logout component
    const [user_id, setUser_Id]: [number , React.Dispatch<React.SetStateAction<number>>] = useState(-1); //This is used in case we need to use the current users id for any future api call or rendering i.e to check the books borrowed by the current user
    const [isLibrarian, setIsLibrarian]: [boolean , React.Dispatch<React.SetStateAction<boolean>>] = useState<boolean>(false); //This is used to render components based on whether or not the user has librarian credentials or not. a user can do create, update or delete operations


    useEffect(() =>{

        const tok = localStorage.getItem('access_token');
        

        if (tok != null){
            const decoded_tok: DecodedToken = jwt_decode(tok);

            setIsAuthenticated(true);
            setUser_Id(decoded_tok.user_id);
            setIsLibrarian(decoded_tok.isLibrarian);
        }
        else{
            setIsAuthenticated(false);
            setUser_Id(-1);
            setIsLibrarian(false);
        }
    },[])

    //This function is called when a user successfully logs in
    const LoginFunction = (access_token: DecodedToken) =>{
        setIsAuthenticated(true);
        setUser_Id(access_token.user_id);
        setIsLibrarian(access_token.isLibrarian);
        console.log("This is also being called for some fucking reason")
    }

    //This is called when a user logs out
    const LogoutFunction = () =>{
        setIsAuthenticated(false);
        setUser_Id(-1);
        setIsLibrarian(false);
        console.log("IsAUthenticated:",isAuthenticated)
        console.log("This is being called (Logout function)")
    }

    return (
        <AuthContext.Provider value={{
                isAuthenticated, 
                user_id,
                isLibrarian, 
                LoginFunction:LoginFunction, 
                LogoutFunction:LogoutFunction
            }
        }>
            {children}
        </AuthContext.Provider>
    )

}

export default AuthContextProvider
