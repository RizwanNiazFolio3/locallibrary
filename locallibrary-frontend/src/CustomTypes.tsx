/**
 * This file contains custom data types and interfaces that are generic enough to be used multiple times throughout the project
 */

export interface AuthorDetails {
    first_name?: string|null,
    last_name?: string|null,
    date_of_birth?: string|null,
    date_of_death?:string|null
}

export interface AuthorAttributes extends AuthorDetails {
    id: number;
}

export type UserLoginData = {
    username:string,
    password:string
}

export type Tokens = {
    access_token:string,
    refresh_token:string
}