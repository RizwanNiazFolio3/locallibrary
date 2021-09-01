import React , {useState} from 'react'
import { Link } from 'react-router-dom'
import LoginComponent from './LoginComponent'

function Navbar() {

    return (
        <div>
            {/* The relative URL for the home page */}
            <p><Link to = '/'>Home</Link></p>
            {/* Relative URL for the book list page (not implemented yet) */}
            <p><Link to = "/books">All books</Link></p>
            {/* Author list page */}
            <p><Link to = "/authors">All authors</Link></p>
            {/* Login page (not implemented yet) */}
            <LoginComponent />
        </div>
    )
}

export default Navbar
