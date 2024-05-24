import { createRouter, createWebHistory } from 'vue-router'
import login from "@/views/login/login.vue";
import home from "@/views/home/home.vue";
import score from "@/views/student/score.vue";
import studentPersonalInfo from "@/views/student/personalInfo.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: login
    },
    {
      path: '/home',
      name: 'home',
      component: home,
      children:[
        {
          path:'score',
          name:'score',
          component:score
        },
        {
          path:'schedule',
          name:'schedule',
          component:()=>import('@/views/student/schedule.vue')
        },
        {
          path:'courseOffering',
          name:'courseOffering',
          component:()=>import('@/views/student/courseOffering.vue')
        },
        {
          path: 'studentProfile',
          name: 'studentProfile',
          component: studentPersonalInfo
        },
        {
          path: 'courseInfo',
          name: 'courseInfo',
          component:()=>import('@/views/teacher/courseInfo.vue')
        },
        {
          path: 'teacherProfile',
          name: 'teacherProfile',
          component:()=>import('@/views/teacher/personalInfo.vue')
        },
        {
          path: 'scoreInput',
          name: 'scoreInput',
          component:()=>import('@/views/teacher/scoreInput.vue')
        },
        {
          path:'studentInfo',
          name:'studentInfo',
          component:()=>import('@/views/admin/studentInfo.vue')
        },
        {
          path:'teacherInfo',
          name:'teacherInfo',
          component:()=>import('@/views/admin/teacherInfo.vue')
        },
        {
          path:'courseOfferingInput',
          name:'courseOfferingInput',
          component:()=>import('@/views/admin/courseOfferingInput.vue')
        },
        {
          path:'studentInfoInput',
          name:'studentInfoInput',
          component:()=>import('@/views/admin/studentInfoInput.vue')
        },
        {
          path:'teacherInfoInput',
          name:'teacherInfoInput',
          component:()=>import('@/views/admin/teacherInfoInput.vue')
        },
        {
          path:'adminProfile',
          name:'adminProfile',
          component:()=>import('@/views/admin/personalInfo.vue')
        }
      ]
    }
  ]
})

export default router
