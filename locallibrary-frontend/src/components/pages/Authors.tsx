import React, {
    useEffect, 
    useState,
    useContext,
} from 'react'
import {client} from "../../axios"
import AuthorListItem from '../AuthorListItem'
import {
    Link,
    useRouteMatch
} from 'react-router-dom'
import {AuthContext} from "../../contexts/AuthContext"
import { AuthorAttributes } from '../../CustomTypes'

function Authors() {
    const {isLibrarian}: {isLibrarian: boolean} = useContext(AuthContext)

    let {url}: {url: string} = useRouteMatch();
    /**
     * This renders the list of authors page.
     * It makes a get request to the authors api end point and saves
     * the recieved data is stored in the state below, it is a list of author objects.
     * The indivisual author objects are then passed to AuthorListItem component
     * as props.
     * The error handling for this component has not been implemented yet.
     */
    const [authorList, setAuthorList] = useState<AuthorAttributes[]>([])

    //When the page first loads up, make an api call to recieve a list of author objects
    //and save it in the state.
    useEffect(() => {
        /**
         * Since we've added "proxy": "http://127.0.0.1:8000/", to packages.json,
         * We do not need to use the full URL and instead a relative URL can be used to access the endpoint
         */
        client.GetAuthorsList()
        .then(AuthorList=>{
            setAuthorList(AuthorList)
        })
    },[])

    //This function returns the AuthorListItem components. It is called in the return statement
    function setAuthorListItemComponent(authorList: AuthorAttributes[]){
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
        const authorListItemComponent: JSX.Element[] = authorList.map(author => {
            if (author.id == null){
                return (
                    <li key = {null}>
                        No items
                    </li>
                )
            }
            else{
                //Passing the link to an authors details page as a prop.
                //The AuthorListItem component then uses the linksto prop to create a link to the authors details page
                return(
                    <li key = {author.id.toString()}>
                        <AuthorListItem 
                            key = {author.id} 
                            item = {author} 
                            linksto = {`${url}/${author.id}`} 
                        />
                    </li>
                ) 
            }
        })
        return authorListItemComponent
    }
    //This creates a link to the librarian creation form page
    function createAuthorLink(){
        return (
            <Link to = {`${url}/create`}>
                Create Author
            </Link>
        )
    }

    return (
        <div>
            <h1>Author List</h1>
            <ul>
                {setAuthorListItemComponent(authorList)}
            </ul>
            {isLibrarian?createAuthorLink():null}
        </div>
    )
}

export default Authors
