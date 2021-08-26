import React from 'react'

function AuthorListItem(props) {
    /**
     * This takes an author object as a prop and
     * Renders out the details to be displayed on the author list page
     */
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

        </>
    )
}

export default AuthorListItem
