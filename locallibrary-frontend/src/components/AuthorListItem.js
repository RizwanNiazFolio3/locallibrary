import React from 'react'

function AuthorListItem(props) {
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
