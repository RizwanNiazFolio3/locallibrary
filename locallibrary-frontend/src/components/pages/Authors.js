import React, {useEffect, useState} from 'react'
import axiosInstance from "../../axios"
import AuthorListItem from '../AuthorListItem'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    useRouteMatch
} from 'react-router-dom'

function Authors() {
    let {path,url} = useRouteMatch();
    /**
     * This renders the list of authors page.
     * It makes a get request to the authors api end point and saves
     * the recieved data is stored in the state below, it is a list of author objects.
     * The indivisual author objects are then passed to AuthorListItem component
     * as props.
     * The error handling for this component has not been implemented yet.
     */
    const [authorList, setAuthorList] = useState([""])

    //When the page first loads up, make an api call to recieve a list of author objects
    //and save it in the state.
    useEffect(() => {
        /**
         * Since we've added "proxy": "http://127.0.0.1:8000/", to packages.json,
         * We do not need to use the full URL and instead a relative URL can be used to access the endpoint
         */
        axiosInstance.get("/catalog/api/authors")
        .then(
            (res) => {setAuthorList(res.data)},
            (error) => {console.log("There was an error retrieving author list")}//Place holder. Will be used for error handling
        )
    },[])

    //This function returns the AuthorListItem components. It is called in the return statement
    function setAuthorListItemComponent(authorList){
        /**
         * Here we use the map method to individually pass the author objects in the authorList as props 
         * to the AuthorListItem component. This gives us a list of such components.
         * In the key field in the <li> tag, we use a ternary operator to set the key value only if the author id
         * is not null i.e the author list has been populated. React needs each <li> item to have a unique key identifier that is
         * a string.
         * When we first load the page, the React Dom renders whatever is in the return statement.
         * When this happens, the useEffect() method is called and the data is retrieved from the api. After which the React Dom
         * renders the component again. As a result, when the component is first rendered, the authorList is not yet populated and
         * is thus empty. Which is why we need to use the ternary operator here to avoid any missing key warnings React might give us
         */
        const authorListItemComponent = authorList.map(author => {
            if (author.id == null){
                return (
                    <li key = {null}>
                        No items
                    </li>
                )
            }
            else{
                return(
                    <li key = {author.id.toString()}>
                        <Link to={`${url}/${parseInt(author.id)}`}>
                            <AuthorListItem key = {author.id} item = {author} />
                        </Link>
                    </li>
                ) 
            }
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
