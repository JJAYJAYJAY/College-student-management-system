<style scoped>
.content{
  width: 100%;
  margin:0 auto;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 20px;
}
.custom-filter {
  padding: 20px;
  background: var(--color-bg-5);
  border: 1px solid var(--color-neutral-3);
  border-radius: var(--border-radius-medium);
  box-shadow: 0 2px 5px rgb(0 0 0 / 10%);
}

.custom-filter-footer {
  display: flex;
  justify-content: space-between;
}
</style>

<template>
  <div>
    <a-space direction="vertical" style="width: 100%">
      <a-row :gutter="80">
        <a-col :span="24">
          <h1>成绩录入</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">成绩详情</h2>
          <a-row>
            <a-col :span="6">
              <a-form-item label="选择课程" :disabled="isDisabled">
                <a-select v-model="selectCourse">
                  <a-option v-for="item in courseList" :key="item" :value="item.courseId">{{item.courseName}}</a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item label="筛选班级" :disabled="isDisabled">
                <a-select :disabled="classDisabled" v-model="selectClass" @change="handleChange">
                  <a-option v-for="item in classList" :key="item" :value="item.classId">{{item.className}}</a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8"></a-col>
            <a-col :span="2">
              <a-button type="primary">下载导入模板</a-button>
            </a-col>
            <a-col :span="2">
             <a-button type="primary">Excel批量导入</a-button>
            </a-col>
          </a-row>
          <a-row style="margin-bottom: 20px">
            <a-col :span="22"></a-col>
            <a-col :span="2">
              <a-button style="width: 120px;" type="primary" @click="handleEditButton">{{buttonText}}</a-button>
            </a-col>
          </a-row>
          <a-table :columns="columns" :data="scoreData" :pagination="{pageSize:13}" :key="freshKey">
            <template #gradeEdit="{record}">
              <div v-if="!showEdit" style="height: 30px">{{record.grade}}</div>
              <a-input-number
                  v-if="showEdit"
                  style="height: 30px"
                  v-model="record.grade"
                  :key="freshKey"
                  @change="handleGradeChange(record)"
              />
            </template>

            <template #name-filter="{ filterValue, setFilterValue, handleFilterConfirm, handleFilterReset}">
              <div class="custom-filter">
                <a-space direction="vertical">
                  <a-input :model-value="filterValue[0]" @input="(value)=>setFilterValue([value])" />
                  <div class="custom-filter-footer">
                    <a-button type="primary" @click="handleFilterConfirm">搜索</a-button>
                    <a-button type="primary" status="danger" @click="handleFilterReset">重置</a-button>
                  </div>
                </a-space>
              </div>
            </template>

          </a-table>
        </div>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">

import {h, onMounted, ref, watch} from "vue";
import {getStudentCourse} from "@/api/student.js";
import useUserStore from "@/stores/userStore.js";
import {getTeacherCourse, teacherGetStudentGrade, updateStudentGrade} from "@/api/teacher.js";
import {IconSearch} from "@arco-design/web-vue/es/icon/index.js";

const columns = ref([
  {
    title: "课程",
    dataIndex: "courseName",
    key: "courseName",
    width: 120,
    align: "center"
  },
  {
    title: "考察方式",
    dataIndex: "testMethod",
    key: "testMethod",
    width: 70,
    align: "center",
  },
  {
    title: "学分",
    dataIndex: "credit",
    key: "credit",
    width: 70,
    align: "center",
  },
  {
    title: "学时",
    dataIndex: "hours",
    key: "hours",
    width: 70,
    align: "center",
  },
  {
    title: "任课班级",
    dataIndex: "className",
    key: "className",
    width: 100,
    align: "center",
  },
  {
    title: "开设学期",
    dataIndex: "term",
    key: "term",
    width: 100,
    align: "center",
  },
  {
    title: "学生姓名",
    dataIndex: "studentName",
    key: "studentName",
    width: 70,
    align: "center",
    filterable: {
      filter: (value, record) => record.studentName.includes(value),
      slotName: 'name-filter',
      icon: () => h(IconSearch)
    }
  },
  {
    title: "学号",
    dataIndex: "studentId",
    key: "studentId",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
  },
  {
    title: "成绩",
    dataIndex: "score",
    key: "score",
    width: 70,
    align: "center",
    sortable: {
      sortDirections: ['ascend', 'descend']
    },
    slotName: 'gradeEdit'
  },
  {
    title: "绩点",
    dataIndex: "point",
    key: "point",
    width: 70,
    align: "center",
    sortable: {
      sortDirections: ['ascend', 'descend']
    },
  }
]);

const classDisabled=ref(true)
const isDisabled=ref(false)
const scoreData=ref([])
const selectClass=ref('')
const selectCourse=ref('')
const classList=ref([])
const courseList=ref([])

const handleChange=()=>{
  teacherGetStudentGrade({
    classId:selectClass.value,
    courseId:selectCourse.value
  }).then(res=>{
    if(res.status===200){
      scoreData.value=res.data.data.studentsScore
    }
  })
}

onMounted(()=>{
  teacherGetStudentGrade({
    classId:selectClass.value,
    courseId:selectCourse.value
  }).then(res=>{
    if(res.status===200){
      courseList.value=res.data.data.courses
    }
  })
})

watch(selectCourse,()=>{
  selectClass.value=''
  teacherGetStudentGrade({
    classId:selectClass.value,
    courseId:selectCourse.value
  }).then(res=>{
    if(res.status===200){
      courseList.value=res.data.data.courses
      classList.value=res.data.data.classes
    }
  })
  if(selectCourse.value===''){
    classDisabled.value=true
  }
  else{
    classDisabled.value=false
  }
})

watch(scoreData,()=>{

})

scoreData.value = [
  {
    courseName: "软件工程",
    testMethod: "考试",
    credit: 3,
    hours: 48,
    className: "软件工程1班",
    term: "2021-2022学年第一学期",
    studentName: "张三",
    studentId: "2018111111",
    grade: 90,
    point: 4.0
  },
  {
    courseName: "软件工程",
    testMethod: "考试",
    credit: 3,
    hours: 48,
    className: "软件工程1班",
    term: "2021-2022学年第一学期",
    studentName: "李四",
    studentId: "2018111112",
    grade: 85,
    point: 3.7
  },
  {
    courseName: "软件工程",
    testMethod: "考试",
    credit: 3,
    hours: 48,
    className: "软件工程1班",
    term: "2021-2022学年第一学期",
    studentName: "王五",
    studentId: "2018111113",
    grade: 80,
    point: 3.3
  },
  {
    courseName: "软件工程",
    testMethod: "考试",
    credit: 3,
    hours: 48,
    className: "软件工程1班",
    term: "2021-2022学年第一学期",
    studentName: "赵六",
    studentId: "2018111114",
    grade: 75,
    point: 3.0
  },
  {
    courseName: "软件工程",
    testMethod: "考试",
    credit: 3,
    hours: 48,
    className: "软件工程1班",
    term: "2021-2022学年第一学期",
    studentName: "钱七",
    studentId: "2018111115",
    grade: 70,
    point: 2.7
  }
]

const freshKey= ref(0)

const handleGradeChange=(record)=>{
  if(record.grade>100){
    record.grade=100
  }
  else if(record.grade<0){
    record.grade=0
  }
  else if(record.grade>=0 && record.grade<=100){}
  else
    record.grade=0
  addChangeData(record)
  record.point = record.grade >= 60 ? (record.grade-50)/10 : 0
  freshKey.value++
}

const showEdit = ref(false)
const buttonText = ref('修改学生成绩')
const changeData = ref([])

const addChangeData = (record)=>{
  // 判断是否已经存在
  for (let i = 0; i < changeData.value.length; i++) {
    if (
        changeData.value[i].studentId === record.studentId &&
        changeData.value[i].courseName === record.courseName &&
        changeData.value[i].term === record.term &&
        changeData.value[i].className === record.className
    ){
      changeData.value[i] = record
      return
    }
  }
  changeData.value.push(record)
}

const handleEditButton = ()=>{
  if(!showEdit.value){
    buttonText.value='保存'
  }
  else{
    console.log('保存成功')
    buttonText.value='修改学生成绩'
    updateStudentGrade({
      data:changeData.value
    }).then(res=>{
      if(res.status===200){
        console.log('保存成功')
      }
      changeData.value=[]
    })
  }
  showEdit.value=!showEdit.value
}

</script>