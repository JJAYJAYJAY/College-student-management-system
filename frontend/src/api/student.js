import axios from 'axios';
import {BASEURL} from "@/api/baseUrl.js";
export function getStudentInfo(){
    return axios.request({
        method: 'post',
        url: '/student/get_student_info',
        baseURL: BASEURL
    })
}

export function getStudentCourse(){
    return axios.request({
        method: 'post',
        url: '/student/get_student_course',
        baseURL: BASEURL
    })
}

export function getStudentGrade(){
    return axios.request({
        method: 'post',
        url: '/student/get_student_grade',
        baseURL: BASEURL
    })
}