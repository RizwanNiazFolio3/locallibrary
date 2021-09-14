import { Link } from 'react-router-dom'
import { BookAttributes } from './BookListContainer'




export const BookListPresentation = (props: { books: BookAttributes[], url: string }) => {
    /*
    * BookListPresentation displays the list of books. It does not have to perform any api calls
    * or computations. It simply displays the content received as properties.
    */

    return (
        <div>
            <ul>
                {
                    props.books.map((book) => (
                        <li key={book.id.toString()}>
                            <Link to={props.url + "/" + book.id.toString()}>

                                {book.title}

                            </Link>
                        </li>
                    ))
                }
            </ul>
        </div>

    )


}
