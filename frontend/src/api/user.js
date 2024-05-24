import axios from 'axios';
import {BASEURL} from "@/api/baseUrl.js";
export function login(data){
    return axios.request({
        method: 'POST',
        url: '/login',
        data: data,
        baseURL: BASEURL
    })
}