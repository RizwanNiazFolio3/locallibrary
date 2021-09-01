import React, {useEffect, useState} from 'react'
import axiosInstance from "../../axios"

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
    const [data, setData] = useState("")

    //This will make a get request to the api once when the page first loads up
    useEffect(() => {
        /**
         * Since we've added "proxy": "http://127.0.0.1:8000/", to packages.json,
         * We do not need to use the full URL and instead a relative URL can be used to access the endpoint
         */
        axiosInstance.get("/catalog/api/home")
        .then(
            (res) => {setData(res.data)},
            (error) => {console.log("An error occured")}
        ) //This should define how the app behaves if the api get request fails
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
