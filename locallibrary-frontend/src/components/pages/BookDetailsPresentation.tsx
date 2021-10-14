import { BookAttributes } from './BookListContainer'
import { Link } from 'react-router-dom'
import { AuthorAttributes } from '../../CustomTypes';
import { GenreMap, LanguageAttributes } from './BookDetailsContainer';


type BookDetailsPresentationProps = {
    book: BookAttributes;
    author: AuthorAttributes;
    language: LanguageAttributes;
    genres: GenreMap;
}


export const BookDetailsPresentation = (props: BookDetailsPresentationProps) => {

    /*
    * BookDetailsPresentation is responsible for displaying all the details of book.
    * It receives the data as properties and does not have to perform any api calls or calculations.
    */


    return (

        <div>

            <h1>Title: {props.book.title}</h1>
            <p>

                <strong>Author: </strong>
                {
                    <Link to={"../authors/" + props.book.author}>
                        {props.author.last_name + ", " + props.author.first_name}
                    </Link>
                }
            </p>
            <p><strong>Summary: </strong> {props.book.summary}</p>
            <p><strong>ISBN: </strong> {props.book.isbn}</p>
            <p><strong>Language: </strong>
                {
                    props.language.name
                }
            </p>
            <p><strong>Genre: </strong> {Object.values(props.genres).map((genre) => genre.name).join(", ")}</p>

        </div>
    );


}
