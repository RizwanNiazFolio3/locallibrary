import React, {useEffect, useState} from 'react'
import {HomePage} from "../../axios"


//After a successful api call, the data element should be populated as HomeData type
type HomeData = {
    num_authors: number;
    num_books: number;
    num_fantasy_genres: number;
    num_instances: number;
    num_instances_available: number;
    num_lotr_books: number;
}


function Home() {
    /**
     * This displays the agregate data needed to be displayed at the home page
     * It collects this data using the API end point for the home page.
     * This home page is a custom api view on the django app.
     * The behaviour in case the api call fails has not been implemented yet.
     * The original Django app also had a counter to keep track of the number of times
     * the home page was visited. This has not been implemented yet either.
     */
    //The state of the component is used to store the JSON data recieved fromt the api end point
    const [data, setData]: [HomeData, React.Dispatch<React.SetStateAction<HomeData>>] = useState({
        num_authors: 0,
        num_books: 0,
        num_fantasy_genres: 0,
        num_instances: 0,
        num_instances_available: 0,
        num_lotr_books: 0
    })

    //This will make a get request to the api once when the page first loads up
    useEffect(() => {
        HomePage(setData)
    },[])

    /**
     * After a successful api call, the data element should be populated as:
     * data = {
     * num_authors: *Some Number*,
     * num_books: *Some Number*,
     * num_fantasy_genres: *Some Number*,
     * num_instances: *Some Number*,
     * num_instances_available: *Some Number*,
     * num_lotr_books: *Some Number*,
     * }
     */

    return (
        <div>
            <h1>Home page</h1>
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
