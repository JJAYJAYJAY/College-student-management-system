import axios from 'axios';
import {BASEURL} from "@/api/baseUrl.js";
export function getTeacherInfo(){
    return axios.request({
        method: 'post',
        url: '/teacher/get_teacher_info',
        baseURL: BASEURL
    })
}

export function getTeacherCourse(){
    return axios.request({
        method: 'post',
        url: '/teacher/get_teacher_course',
        baseURL: BASEURL
    })
}