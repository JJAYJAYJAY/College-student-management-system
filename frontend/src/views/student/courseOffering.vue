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
          <h1>开班信息查询</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">

          <h2 style="margin-bottom: 20px">开班详情</h2>
          <a-col :span="6">
            <a-form-item label="筛选班级" :disabled="isDisabled">
              <a-select v-model="selectClass" @change="handleChange">
                <a-option v-for="item in classList" :key="item" :value="item.classId">{{item.className}}</a-option>
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
import {getCourseOffering, getStudentCourse} from "@/api/student.js";

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


const classList=ref([])

const selectClass=ref('')
const isDisabled=ref(false)
const scheduleData=ref([])
const handleChange=()=>{
  getCourseOffering({
    classId:selectClass.value
  }).then(res=>{
    if(res.status===200){
      scheduleData.value=res.data.data.detailCourse
    }
  })
}

onMounted(()=>{
  getCourseOffering({
    classId:selectClass.value
  }).then(res=>{
    if(res.status===200){
      classList.value=res.data.data.allCourse
    }
  })
})
</script>