<style scoped>

</style>

<template>
  <div>
    <a-space direction="vertical" style="width: 100%;">
      <a-row :gutter="80">
        <a-col :span="16">
          <a-descriptions :data="studentData" size="large" title="个人信息" :column="1"/>
        </a-col>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">
import {onMounted, ref} from "vue";
import {getTeacherInfo} from "@/api/teacher.js";

const studentData=ref([])

const CHINESE_DICT = {
  'teacherId': '教师号',
  'teacherName': '姓名',
  'sex': '性别',
  'age': '年龄',
  'jobTitle': '已修学分',
  'phone': '手机号'
}
onMounted(()=>{
  getTeacherInfo().then(res=>{
    if(res.status===200){
      studentData.value=Object.keys(res.data.data).map(key=>{
        return {
          label: CHINESE_DICT[key],
          value: res.data.data[key]
        }
      })
    }
  })
})
</script>