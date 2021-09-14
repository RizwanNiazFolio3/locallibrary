import React, {useState, useEffect} from 'react'
import axios from 'axios'
import { useRouteMatch } from 'react-router'
import { BookListPresentation } from './BookListPresentation'

// The attributes of a single book
export type BookAttributes = {
    id: number;
    title: string;
    author: number;
    summary: string;
    isbn: string;
    language: number;
    genre: number[];
}


export const BookListContainer = () => {
    /*
    * BookListContainer is responsible for all computations and api calls to fetch the list of all books.
    * Once all details are fetched, it delegates the task of presention to BookListPresentation.
    */

    let {url}: {url: string} = useRouteMatch(); // The url of this page
    let [books, setBooks]: [BookAttributes[] | undefined,
        React.Dispatch<React.SetStateAction<BookAttributes[] | undefined>>] = useState();   // The list of books


    useEffect(() => {

        //Fetching the list of books using api call
        axios.get("/catalog/api/books/")
        .then(
            (result) => { setBooks(result.data);},
            (error) => {console.log(`Error! Could not fetch list of books.`)}
        )

    }, []);

    if(!books){
        return <div>Loading...</div>
    }
    return (
        // Book list is presented once the list of books is properly initialized
        <BookListPresentation books={books} url={url}/>
    )


}