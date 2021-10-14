import React, {useContext} from 'react'
import {
    Link,
    useRouteMatch
} from "react-router-dom"
import {AuthContext} from "../contexts/AuthContext"


// The attributes of a single author
export interface Author {
    id: number;
    first_name: string;
    last_name: string;
    date_of_birth: string;
    date_of_death: string;
}


// The properties received by this component
export type AuthorListItemProps = {
    key: number; 
    item: Author; 
    linksto: string; 
}

function AuthorListItem(props: AuthorListItemProps) {
    /**
     * This takes an author object as a prop and
     * Renders out the details to be displayed on the author list page
     */
    const {url}: {url: string} = useRouteMatch()
    const {isLibrarian}: {isLibrarian: boolean} = useContext(AuthContext)

    //This function runs if the current user is a librarian. i.e has permission to edit or delete an authors details
    function librarianLinks(){
        return (
            <>
                <Link to={`${url}/${props.item.id}/update`} style={{color:'orange'}}>
                    {" "}Update{" "}
                </Link>
                <Link to={`${url}/${props.item.id}/delete`} style={{color:'red'}}>
                    Delete 
                </Link>
            </>
        )
    }

    return (
        <>
        <Link to={props.linksto}>
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
        </Link>
            {isLibrarian === true? librarianLinks(): null}
        </>
    )
}

export default AuthorListItem
