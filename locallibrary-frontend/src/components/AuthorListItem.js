import React, {useEffect, useState} from 'react'
import {
    Link,
    useRouteMatch
} from "react-router-dom"
import jwt_decode from "jwt-decode";


function AuthorListItem(props) {
    /**
     * This takes an author object as a prop and
     * Renders out the details to be displayed on the author list page
     */
    const {url} = useRouteMatch()
    // const [isLibrarian,setIsLibrarian] = useState(false)

    // useEffect(() =>{
    //     if (localStorage.getItem("access_token")){
    //         let token = jwt_decode(localStorage.getItem("access_token"))
    //         console.log(token)
    //         if (token.isLibrarian == true){
    //             setIsLibrarian(true)
    //         }
    //     }
    // },[])

    function librarianLinks(){
        console.log("Here")
        return (
            <>
                <Link to={`${url}/${parseInt(props.item.id)}/update`} style={{color:'orange'}}>
                    {" "}Update{" "}
                </Link>
                <Link to={`${url}/${parseInt(props.item.id)}/delete`} style={{color:'red'}}>
                    Delete 
                </Link>
            </>
        )
    }

    return (
        <>
            {props.item.last_name},
            {props.item.first_name}
            <span>
            {"("}
                <span style = {{fontWeight:'bold'}}>
                    {(props.item.date_of_birth == null ) ? "--": props.item.date_of_birth.replace(/-/g,"/")}
                </span>
                {" "}
                -
                {" "}
                <span style = {{fontWeight:"bold"}}>
                    {(props.item.date_of_death == null ) ? "--": props.item.date_of_death.replace(/-/g,"/")}
                </span>
            {")"}
            </span>
            {localStorage.getItem('isLibrarian') == "true"? librarianLinks(): null}
        </>
    )
}

export default AuthorListItem
