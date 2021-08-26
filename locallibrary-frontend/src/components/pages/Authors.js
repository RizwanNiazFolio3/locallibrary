import React, {useEffect, useState} from 'react'
import axios from "axios"
import AuthorListItem from '../AuthorListItem'

function Authors() {
    const [authorList, setAuthorList] = useState([""])

    useEffect(() => {
        axios.get("catalog/api/authors")
        .then(
            (res) => {setAuthorList(res.data)},
            (error) => {console.log("There was an error retrieving author list")}
        )
    },[])


    function setAuthorListItemComponent(authorList){
        const authorListItemComponent = authorList.map(author => {
                return <li key = {(author.id != null) ? author.id.toString() : null}>
                    <AuthorListItem key = {author.id} item = {author} />
                    </li>
        })
        return authorListItemComponent
    }

    return (
        <div>
            <h1>Author List</h1>
            <ul>
                {setAuthorListItemComponent(authorList)}
            </ul>
        </div>
    )
}

export default Authors
