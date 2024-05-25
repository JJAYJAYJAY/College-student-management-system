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

export function adminGetTeacherInfo(){
    return axios.request({
        method: 'post',
        url: '/admin/admin_get_teacher_info',
        baseURL: BASEURL
    })
}

export function adminGetStudentChangeInfo(){
    return axios.request({
        method: 'post',
        url: '/admin/admin_get_student_change_info',
        baseURL: BASEURL
    })
}

export function updateStudentInfo(data){
    return axios.request({
        method: 'post',
        url: '/admin/update_student_info',
        baseURL: BASEURL,
        data
    })
}

export function deleteStudentInfo(data){
    return axios.request({
        method: 'post',
        url: '/admin/delete_student_info',
        baseURL: BASEURL,
        data
    })
}

export const updateStudentInfoFromExcel = BASEURL + '/admin/update_student_info_from_excel';


export function adminGetTeacherChangeInfo(){
    return axios.request({
        method: 'post',
        url: '/admin/admin_get_teacher_change_info',
        baseURL: BASEURL
    })
}

export function updateTeacherInfo(data){
    return axios.request({
        method: 'post',
        url: '/admin/update_teacher_info',
        baseURL: BASEURL,
        data
    })
}

export function deleteTeacherInfo(data){
    return axios.request({
        method: 'post',
        url: '/admin/delete_teacher_info',
        baseURL: BASEURL,
        data
    })
}

export const updateTeacherInfoFromExcel = BASEURL + '/admin/update_teacher_info_from_excel';