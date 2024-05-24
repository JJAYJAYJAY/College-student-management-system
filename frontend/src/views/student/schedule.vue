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
          <h1>课表查询</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">
            班级信息
          </h2>
          <a-descriptions style="margin-bottom: 20px" :data="classData" size="large" bordered />
          <h2 style="margin-bottom: 20px">课表详情</h2>
          <a-col :span="6">
            <a-form-item label="筛选学期" :disabled="isDisabled">
              <a-select v-model="selectTerm" @change="handleChange">
                <a-option v-for="item in termList" :key="item" :value="item">{{item}}</a-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-table :columns="columns" :data="scheduleData"  :pagination="{pageSize:13}"></a-table>
        </div>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">

import {onMounted, ref} from "vue";
import {getStudentCourse} from "@/api/student.js";
import useUserStore from "@/stores/userStore.js";

const columns = ref([
  {
    title: "课程",
    dataIndex: "CourseName",
    key: "CourseName",
    width: 200,
    align: "center"
  },
  {
    title: "考察方式",
    dataIndex: "TestMethod",
    key: "TestMethod",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "学分",
    dataIndex: "Credit",
    key: "Credit",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
  },
  {
    title: "学时",
    dataIndex: "Hours",
    key: "Hours",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
  },
  {
    title: "任课教师",
    dataIndex: "TeacherName",
    key: "TeacherName",
    width: 100,
    align: "center",
  },
  {
    title: "开设学期",
    dataIndex: "Term",
    key: "Term",
    width: 100,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
  }
]);

const classData = ref([
  {
    label: "班级号",
    value: "C01"
  },
  {
    label:"专业",
    value:"软件工程"
  },
  {
    label: "班级",
    value: "软件工程1班"
  },
]);

const termList=ref([])

const selectTerm=ref('')
const isDisabled=ref(false)
const scheduleData=ref([])
const userStore = useUserStore();
const handleChange=()=>{
  getStudentCourse({
    term:selectTerm.value,
    classId:userStore.user.classId
  }).then(res=>{
    if(res.status===200){
      scheduleData.value=res.data.data.course
    }
  })
}

onMounted(()=>{
  getStudentCourse({
    term:'',
    classId:userStore.user.classId
  }).then(res=>{
    if(res.status===200){
      for (let i = 0; i < res.data.data.term.length; i++) {
        termList.value.push(res.data.data.term[i].Term)
      }
    }
  })
})
</script>