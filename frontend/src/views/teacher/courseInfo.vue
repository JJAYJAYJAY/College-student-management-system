<style scoped>
.content{
  width: 100%;
  margin:0 auto;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 20px;
}
</style>

<template>
  <div>
    <a-space direction="vertical" style="width: 100%">
      <a-row :gutter="80">
        <a-col :span="24">
          <h1>任课信息查询</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">任课详情</h2>
          <a-table :columns="columns" :data="scheduleData"  :pagination="{pageSize:13}"></a-table>
        </div>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">

import {onMounted, ref, watch} from "vue";
import {getStudentCourse} from "@/api/student.js";
import useUserStore from "@/stores/userStore.js";
import {getTeacherCourse} from "@/api/teacher.js";

const columns = ref([
  {
    title: "课程",
    dataIndex: "courseName",
    key: "courseName",
    width: 200,
    align: "center"
  },
  {
    title: "考察方式",
    dataIndex: "testMethod",
    key: "testMethod",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter: (value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.testMethod === value[i]) {
            return true
          }
        }
      },
    }
  },
  {
    title: "学分",
    dataIndex: "credit",
    key: "credit",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter: (value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.credit === value[i]) {
            return true
          }
        }
      },
    }
  },
  {
    title: "学时",
    dataIndex: "hours",
    key: "hours",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter: (value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.hours === value[i]) {
            return true
          }
        }
      },
    }
  },
  {
    title: "任课班级",
    dataIndex: "className",
    key: "className",
    width: 100,
    align: "center",
    sortable: {
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter: (value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.className === value[i]) {
            return true
          }
        }
      },
    }
  },
  {
    title: "开设学期",
    dataIndex: "term",
    key: "term",
    width: 100,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter: (value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.term === value[i]) {
            return true
          }
        }
      },
    }
  }
]);


const isDisabled=ref(false)
const scheduleData=ref([])

const handleChange=()=>{

}

onMounted(()=>{
  getTeacherCourse().then(res=>{
    if(res.status===200){
      scheduleData.value=res.data.data.course
    }
  })
})

watch(scheduleData,()=>{
  //统计学期类型
  let termSet=new Set()
  scheduleData.value.forEach(item=>{
    termSet.add(item.term)
  })
  termSet=Array.from(termSet)
  columns.value[5].filterable.filters=termSet.map(item=>{
    return {
      text:item,
      value:item
    }
  })
  //统计考察方式
  let testMethodSet=new Set()
  scheduleData.value.forEach(item=>{
    testMethodSet.add(item.testMethod)
  })
  testMethodSet=Array.from(testMethodSet)
  columns.value[1].filterable.filters=testMethodSet.map(item=>{
    return {
      text:item,
      value:item
    }
  })
  //统计学分
  let creditSet=new Set()
  scheduleData.value.forEach(item=>{
    creditSet.add(item.credit)
  })
  creditSet=Array.from(creditSet)
  columns.value[2].filterable.filters=creditSet.map(item=>{
    return {
      text:item,
      value:item
    }
  })
  //统计学时
  let hourSet=new Set()
  scheduleData.value.forEach(item=>{
    hourSet.add(item.hours)
  })
  hourSet=Array.from(hourSet)
  columns.value[3].filterable.filters=hourSet.map(item=>{
    return {
      text:item,
      value:item
    }
  })
  //统计班级
  let classSet=new Set()
  scheduleData.value.forEach(item=>{
    classSet.add(item.className)
  })
  classSet=Array.from(classSet)
  columns.value[4].filterable.filters=classSet.map(item=>{
    return {
      text:item,
      value:item
    }
  })
})
</script>