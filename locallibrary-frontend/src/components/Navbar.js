import React from 'react'
import { Link } from 'react-router-dom'

function Navbar() {
    return (
        <div>
            <p><Link to = '/'>Home</Link></p>
            <p><Link to = "books">All books</Link></p>
            <p><Link to = "authors">All authors</Link></p>
            <p><Link to = "Login">Login</Link></p>
        </div>
    )
}

export default Navbar
