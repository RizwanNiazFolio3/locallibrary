import React, { useEffect, useState } from 'react'
import axios from '../../axios'
import { BookAttributes } from './BookListContainer'
import { useParams } from 'react-router'
import { AuthorAttributes } from '../AuthorListItem'
import { BookDetailsPresentation } from './BookDetailsPresentation'


// The properties of Genre are stored in this type
export type GenreAttributes = {
    id: number;
    name: string;
}


// GenreMap represents a map of Genre items. Id of genre is used as key
export type GenreMap = {
    [id: number]: GenreAttributes;
}


// The properties of a language are stored in this type
export type LanguageAttributes = {
    id: number;
    name: string;
}

export const BookDetailsContainer = () => {
    /*
    * BookDetailsContainer performs all the computation and api calls to fetch book details.
    * It delegates the task of actually displaying the data to BookDetailsPresentation.
    */

    //id is extracted from url
    let { id }: { id: string } = useParams();



    // book, genre and language are intentially allowed to be undefined. We display the page once these values are loaded


    let [book, setBook]: [BookAttributes | undefined,
        React.Dispatch<React.SetStateAction<BookAttributes | undefined>>] = useState(); //The book to be displayed

    let [genres, setGenres]:
        [GenreMap, React.Dispatch<React.SetStateAction<GenreMap>>] = useState({});  // Genre of the book

    let [author, setAuthor]: [AuthorAttributes | undefined,
        React.Dispatch<React.SetStateAction<AuthorAttributes | undefined>>] = useState();   // Author of the book

    let [language, setLanguage]: [LanguageAttributes | undefined,
        React.Dispatch<React.SetStateAction<LanguageAttributes | undefined>>] = useState(); // Language of the book



    useEffect(() => {

        // Getting value of book from the api
        axios.get(`/catalog/api/books/${id}/`)
            .then(
                (result) => {
                    setBook(result.data);
                },
                (error) => { console.log(`Error! The book with id ${id} does not exist.`) }
            )

    }, [id]);


    useEffect(() => {

        if (book) {
            // This effect takes action once the book is properly loaded

            // Fetching the author of this book from api
            axios.get(`/catalog/api/authors/${book.author}`)
                .then(
                    (resultAuthor) => {
                        setAuthor(resultAuthor.data);
                    },
                    (errorAuthor) => { console.log(`Error! Author for book with id ${id} does not exist`) }
                )
        }


    }, [book, id]);


    useEffect(() => {

        if (book) {
            // This effect takes action once the book is properly loaded

            for (const genre of book.genre) {
                // Fetching each genre using a individual api calls

                axios.get(`/catalog/api/genres/${genre}`)
                    .then(
                        (resultGenre) => {

                            setGenres((prevGenres: GenreMap) => ({
                                ...prevGenres,
                                [genre]: resultGenre.data
                            }));
                        },
                        (errorGenre) => { console.log(`Error! Genre ${genre} for book with id ${id} does not exist`) }
                    )
            }
        }

    }, [book, id]);


    useEffect(() => {

        if (book) {
            // This effect takes action once the book is properly loaded

            // Fetching the language of this book using api
            axios.get(`/catalog/api/languages/${book.language}`)
                .then(
                    (resultLanguage) => {

                        setLanguage(resultLanguage.data);
                    },
                    (errorGenre) => { console.log(`Error! Language for book with id ${id} does not exist`) }
                )

        }

    }, [book, id]);


    if (!book || !author || !language) {

        return <div>Loading...</div>
    }
    else {
        // The book details are presented once all details have been received
        return <BookDetailsPresentation book={book} author={author} language={language} genres={genres} />
    }

}
