import React, {
    useEffect, 
    useState, 
    useContext
} from 'react'
import {
    useParams,
    Link,
    useRouteMatch,
  } from "react-router-dom";
  
import {GetAuthorDetails} from '../../axios';
import {AuthContext} from "../../contexts/AuthContext"


function AuthorDetails() {
    //Getting the id of the author from the url of the current page as a parameter
    let {id}:{id: string} = useParams();
    const {url}: {url: string} = useRouteMatch()

    const {isLibrarian}: {isLibrarian: boolean} = useContext(AuthContext)

    const [firstName,setFirstName] = useState("")
    const [lastName,setLastName] = useState("")
    const [dateOfBirth,setDateOfBirth] = useState("")
    const [dateOfDeath,setDateOfDeath] = useState("")

    //Getting the details of a specific author from the api endpoint
    useEffect(() => {
        GetAuthorDetails(id,setFirstName,setLastName,setDateOfBirth,setDateOfDeath)
    },[id])

    //This creates links to the update and delete librarian pages
    function librarianLinks(){
        return (
            <>
                <Link to={`${url}/update`} style={{color:'orange'}}>
                    {" "}Update{" "}
                </Link>
                <Link to={`${url}/delete`} style={{color:'red'}}>
                    Delete 
                </Link>
            </>
        )
    }

    //Rendering out the Author page. 
    //The Book Description portion is a placeholder as the api to get the books for an author has not been made yet
    return (
        <div>
            <h1>Author: {lastName}, {firstName}</h1>
            {isLibrarian === true? librarianLinks(): null}
            <p>({dateOfBirth ? dateOfBirth.replace(/-/g,"/") : "-"} to {dateOfDeath ? dateOfDeath.replace(/-/g,"/") : "-"})</p>
            <div>
                <h3>Books</h3>
                <ul>
                    <li style={{fontWeight:"bold"}}>Placeholder for book title</li>
                    <p>Book description</p>
                </ul>
            </div>
        </div>
    )
}

export default AuthorDetails
