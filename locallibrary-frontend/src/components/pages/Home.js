import React, {useEffect, useState} from 'react'
import axios from "axios"

function Home() {
    const [data, setData] = useState("")

    useEffect(() => {
        axios.get("catalog/api/home")
        .then(
            (res) => {setData(res.data)},
            (error) => {console.log("An error occured")})
    },[])

    return (
        <div>
            <p>Authors: {data.num_authors}</p>
            <p>Books: {data.num_books}</p>
            <p>Fantasy Subgenres: {data.num_fantasy_genres}</p>
            <p>Copies of Books: {data.num_instances}</p>
            <p>Copies available for borrowing: {data.num_instances_available}</p>
            <p>lord of the rings books: {data.num_lotr_books}</p>
            Home page stuff goes here
        </div>
    )
}

export default Home
