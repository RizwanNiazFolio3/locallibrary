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
  
  import {client} from '../../axios';
  import {AuthContext} from "../../contexts/AuthContext"


function AuthorDetails() {
    //Getting the id of the author from the url of the current page as a parameter
    let {id}:{id: string} = useParams();
    const {url}: {url: string} = useRouteMatch()

    const {isLibrarian}: {isLibrarian: boolean} = useContext(AuthContext)

    const [firstName,setFirstName] = useState<string|null|undefined>("")
    const [lastName,setLastName] = useState<string|null|undefined>("")
    const [dateOfBirth,setDateOfBirth] = useState<string|null|undefined>("")
    const [dateOfDeath,setDateOfDeath] = useState<string|null|undefined>("")

    //Getting the details of a specific author from the api endpoint
    useEffect(() => {
        client.GetAuthorDetails(id)
        .then(
            response => {
                setFirstName(response.first_name)
                setLastName(response.last_name)
                setDateOfBirth(response.date_of_birth)
                setDateOfDeath(response.date_of_death)
            }
        )
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
