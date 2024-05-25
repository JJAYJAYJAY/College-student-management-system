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
          <h1>学生信息管理</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">学生信息详情</h2>
          <a-row style="margin-bottom: 20px">
            <a-col :span="6">
<!--              <a-form-item label="选择课程" :disabled="isDisabled">-->
<!--                <a-select v-model="selectCourse">-->
<!--                  <a-option v-for="item in courseList" :key="item" :value="item.courseId">{{item.courseName}}</a-option>-->
<!--                </a-select>-->
<!--              </a-form-item>-->
            </a-col>
            <a-col :span="6">
<!--              <a-form-item label="筛选班级" :disabled="isDisabled">-->
<!--                <a-select :disabled="classDisabled" v-model="selectClass" @change="handleChange">-->
<!--                  <a-option v-for="item in classList" :key="item" :value="item.classId">{{item.className}}</a-option>-->
<!--                </a-select>-->
<!--              </a-form-item>-->
            </a-col>
            <a-col :span="8"></a-col>
            <a-col :span="2">
              <a href="/学生信息导入模板.xlsx" download>
                <a-button type="primary">下载导入模板</a-button>
              </a>
            </a-col>
            <a-col :span="2">
              <a-button type="primary" @click="uploadVisible=true">Excel批量导入</a-button>
              <a-modal :visible="uploadVisible" @ok="handleOk" @cancel="handleUploadCancel" style="position: absolute">
                <template #title>
                  Excel导入
                </template>
                <div>
                  <a-upload
                      ref="upload"
                      :action="updateStudentInfoFromExcel"
                      draggable
                      :auto-upload="false"
                      accept="application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                      limit="1"
                      @success="onFileSuccess"
                      @error="onFileError"
                      :headers="{'Authorization': 'Bearer ' + token}"
                  />
                </div>
              </a-modal>
            </a-col>
          </a-row>
          <a-row style="margin-bottom: 20px">
            <a-col :span="22"></a-col>
            <a-col :span="2">
              <a-button style="width: 120px;" type="primary" @click="handleEditButton">{{buttonText}}</a-button>
            </a-col>
          </a-row>
          <a-table :columns="columns" :data="studentData" :pagination="{pageSize:13}" :key="freshKey">
            <template #nameEdit="{record}">
              <div v-if="!showEdit" style="height: 30px">{{record.studentName}}</div>
              <a-input
                  v-if="showEdit"
                  style="height: 30px"
                  v-model="record.studentName"
                  :key="freshKey"
                  @change="addChangeData(record)"
              />
            </template>

            <template #sexEdit="{record}">
              <div v-if="!showEdit" style="height: 30px">{{record.sex}}</div>
              <a-select
                  v-if="showEdit"
                  style="height: 30px"
                  v-model="record.sex"
                  :key="freshKey"
                  @change="addChangeData(record)"
              >
                <a-option>男</a-option>
                <a-option>女</a-option>
              </a-select>
            </template>

            <template #ageEdit="{record}">
              <div v-if="!showEdit" style="height: 30px">{{record.age}}</div>
              <a-input-number
                  v-if="showEdit"
                  style="height: 30px"
                  v-model="record.age"
                  :key="freshKey"
                  @change="addChangeData(record)"
              />
            </template>

            <template #regionEdit="{record}">
              <div v-if="!showEdit" style="height: 30px">{{record.region}}</div>
              <a-select
                  v-if="showEdit"
                  style="height: 30px"
                  v-model="record.region"
                  :key="freshKey"
                  allow-search
                  @change="addChangeData(record)"
              >
                <a-option v-for="item in provinces">{{item}}</a-option>
              </a-select>
            </template>

            <template #classEdit="{record}">
              <div v-if="!showEdit" style="height: 30px">{{record.className}}</div>
              <a-select
                  v-if="showEdit"
                  style="height: 30px"
                  v-model="record.classId"
                  :key="freshKey"
                  @change="addChangeData(record)"
              >
                <a-option v-for="item in classList" :key="item" :value="item.classId">{{item.className}}</a-option>
              </a-select>
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
            <template #delete="{record}">
              <a-popconfirm content="你确定要删除该位学生吗？" @ok="deleteStudent(record.studentId)" position="lt">
                <a-button type="primary" status="danger">删除</a-button>
              </a-popconfirm>
            </template>
          </a-table>
        </div>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">

import {h, onMounted, ref, watch} from "vue";
import {IconSearch} from "@arco-design/web-vue/es/icon/index.js";
import {Message} from "@arco-design/web-vue";
import {provinces} from "@/constant/provinces.js";
import {
  adminGetStudentChangeInfo,
  deleteStudentInfo,
  updateStudentInfo,
  updateStudentInfoFromExcel
} from "@/api/admin.js";

const columns = ref([
  {
    title: "学号",
    dataIndex: "studentId",
    key: "studentId",
    width: 120,
    align: "center"
  },
  {
    title: "姓名",
    dataIndex: "studentName",
    key: "studentName",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filter: (value, record) => record.studentName.includes(value),
      slotName: 'name-filter',
      icon: () => h(IconSearch)
    },
    slotName: 'nameEdit'
  },
  {
    title: "性别",
    dataIndex: "sex",
    key: "sex",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter:(value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.sex === value[i]) {
            return true
          }
        }
      },
    },
    slotName: 'sexEdit'
  },
  {
    title: "年龄",
    dataIndex: "age",
    key: "age",
    width: 50,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    slotName: 'ageEdit'
  },
  {
    title: "生源地",
    dataIndex: "region",
    key: "region",
    width: 80,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter:(value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.region === value[i]) {
            return true
          }
        }
      },
    },
    slotName: 'regionEdit'
  },
  {
    title: "专业",
    dataIndex: "majorName",
    key: "majorName",
    width: 150,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter:(value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.majorName === value[i]) {
            return true
          }
        }
      },
    }
  },
  {
    title: "班级",
    dataIndex: "className",
    key: "className",
    width: 150,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter:(value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.className === value[i]) {
            return true
          }
        }
      },
    },
    slotName: 'classEdit'
  },
  {
    title: "删除",
    dataIndex: "operation",
    key: "operation",
    width: 100,
    align: "center",
    slotName: 'delete'
  }
]);


const isDisabled=ref(false)
const studentData=ref([])
const classList=ref([])
const uploadVisible=ref(false)
const upload=ref()
const token=sessionStorage.getItem('token')

onMounted(()=> {
  adminGetStudentChangeInfo().then(res => {
    if (res.status === 200) {
      studentData.value = res.data.data.students
      classList.value = res.data.data.classes
    }
  })
})


studentData.value = []

const freshKey= ref(0)
const showEdit = ref(false)
const buttonText = ref('修改学生信息')
const changeData = ref([])

const addChangeData = (record)=>{
  // 判断是否已经存在
  for (let i = 0; i < changeData.value.length; i++) {
    if (changeData.value[i].studentId === record.studentId) {
      changeData.value[i] = record
      return
    }
  }
  changeData.value.push(record)
}

const handleEditButton = ()=>{
  showEdit.value = !showEdit.value
  if(showEdit.value){
    buttonText.value = '保存修改'
  }else{
    buttonText.value = '修改学生信息'
    // 提交修改
    updateStudentInfo({
      data: changeData.value
    }).then(
      res=>{
        if(res.status===200){
          Message.success("修改成功")
          adminGetStudentChangeInfo().then(res=>{
            if(res.status===200){
              studentData.value = res.data.data.students
              classList.value = res.data.data.classes
            }
          })
        }
      }
    )
    // 提交成功后
    showEdit.value = false
  }
}

const handleUploadCancel=()=>{
  uploadVisible.value=false
}


const handleOk=()=>{
  upload.value.submit()
}

const onFileSuccess=(res)=>{
  Message.success("上传成功")
  uploadVisible.value=false
}

const onFileError=()=>{
  Message.error("上传失败")
}

const deleteStudent=(studentId)=>{
  deleteStudentInfo({
    studentId: studentId
  }).then(res=>{
    if(res.status===200){
      Message.success("删除成功")
      adminGetStudentChangeInfo().then(res=>{
        if(res.status===200){
          studentData.value = res.data.data.students
          classList.value = res.data.data.classes
        }
      })
    }
  })
}
</script>