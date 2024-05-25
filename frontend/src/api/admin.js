import axios from 'axios';
import {BASEURL} from "@/api/baseUrl.js";
export function getAdminInfo(){
    return axios.request({
        method: 'post',
        url: '/admin/get_admin_info',
        baseURL: BASEURL
    })
}

export function adminGetStudentInfo(){
    return axios.request({
        method: 'post',
        url: '/admin/admin_get_student_info',
        baseURL: BASEURL
    })
}

export function getTeacherInfo(){
    return axios.request({
        method: 'post',
        url: '/admin/get_teacher_info',
        baseURL: BASEURL
    })
}


