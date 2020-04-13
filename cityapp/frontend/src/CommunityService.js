import axios from 'axios/index';
import apiClient from './util/ApiClient';
const API_URL = 'http://localhost:8000';

export default class CustomersService{

    constructor(){}


    getPosts() {
        const url = `${API_URL}/api/community/community/latest-posts/`;
        return apiClient.get(url).then(response => response.data);
    }

}