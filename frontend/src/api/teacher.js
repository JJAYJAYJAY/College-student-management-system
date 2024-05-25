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

export function teacherGetStudentGrade(data){
    return axios.request({
        method: 'post',
        data:data,
        url: '/teacher/teacher_get_student_grade',
        baseURL: BASEURL
    })
}

export function updateStudentGrade(data){
    return axios.request({
        method: 'post',
        data:data,
        url: '/teacher/update_student_grade',
        baseURL: BASEURL
    })
}

export const updateStudentFromExcel = BASEURL + '/teacher/update_student_from_excel';