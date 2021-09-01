import React, {useEffect, useState} from 'react'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    useParams
  } from "react-router-dom";
  
  import axiosInstance from '../../axios';


function AuthorDetails() {
    let {id} = useParams();
    console.log(id)

    const [firstName,setFirstName] = useState("")
    const [lastName,setLastName] = useState("")
    const [dateOfBirth,setDateOfBirth] = useState("")
    const [dateOfDeath,setDateOfDeath] = useState("")

    useEffect(() => {
        
        console.log("catalog/api/authors/")
        axiosInstance.get("/catalog/api/authors/"+id)
        .then(response =>{
            setFirstName(response.data.first_name)
            setLastName(response.data.last_name)
            setDateOfBirth(response.data.date_of_birth)
            setDateOfDeath(response.data.date_of_death)
        })
    },[])
    return (
        <div>
            <h1>Author: {lastName}, {firstName}</h1>
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
