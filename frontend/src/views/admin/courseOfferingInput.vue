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
          <h1>开课信息管理</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">开课信息详情</h2>
          <a-row style="margin-bottom: 20px">
            <a-col :span="6">
              <a-form-item label="选择专业">
                <a-select v-model="selectMajor">
                  <a-option v-for="item in majorList" :key="item" :value="item.majorId">{{item.majorName}}</a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item label="选择班级">
                <a-select v-model="selectClass" @change="handleChange" >
                  <a-option v-for="item in classData[selectMajor]" :key="item" :value="item.classId">{{item.className}}</a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8"></a-col>
            <a-col :span="2">
              <a href="/开课信息导入模板.xlsx" download>
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
                      :action="updateCourseInfoFromExcel"
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
          <a-table :columns="columns" :data="courseData" :pagination="{pageSize:13}" :key="freshKey">
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
              <a-popconfirm content="你确定要删除这条开课信息吗？" @ok="deleteCourse(record.classId,record.courseId)" position="lt">
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

import { onMounted, ref, watch} from "vue";
import {Message} from "@arco-design/web-vue";
import {
  adminGetCourseInfo, deleteCourseInfo, updateCourseInfoFromExcel,
} from "@/api/admin.js";

const columns = ref([
  {
    title: "专业",
    dataIndex: "majorName",
    key: "majorName",
    width: 120,
    align: "center"
  },
  {
    title: "班级",
    dataIndex: "className",
    key: "className",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "课程",
    dataIndex: "courseName",
    key: "courseName",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "考察方式",
    dataIndex: "testMethod",
    key: "testMethod",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "学分",
    dataIndex: "credit",
    key: "credit",
    width: 50,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "学时",
    dataIndex: "hours",
    key: "hours",
    width: 80,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
  },
  {
    title: "开设学期",
    dataIndex: "term",
    key: "term",
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
          if (record.term === value[i]) {
            return true
          }
        }
      },
    }
  },
  {
    title: "教师",
    dataIndex: "teacherName",
    key: "teacherName",
    width: 100,
    align: "center"
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


const majorList=ref([])
const classData=ref([])
const selectMajor=ref('')
const selectClass=ref('')
const courseData=ref([])
const uploadVisible=ref(false)
const upload=ref()
courseData.value = []
const token=sessionStorage.getItem('token')

onMounted(()=> {
  adminGetCourseInfo({}).then(res=>{
    if(res.status===200){
      majorList.value=res.data.data.majorData
      classData.value=res.data.data.classData
    }
  })
})

watch(courseData,(newData)=>{
  //统计学期类型
  let termSet = new Set()
  for (let i = 0; i < newData.length; i++) {
    termSet.add(newData[i].term)
  }
  let termList = Array.from(termSet)
  columns.value[6].filterable.filters = termList.map(item => {
    return {
      text: item,
      value: item
    }
  })
})

const handleChange=()=> {
  courseData.value = []
  adminGetCourseInfo({
    classId: selectClass.value
  }).then(res => {
    if (res.status === 200) {
      majorList.value=res.data.data.majorData
      classData.value=res.data.data.classData
      courseData.value = res.data.data.courseData
    }
  })
}

const freshKey= ref(0)
const showEdit = ref(false)
const buttonText = ref('添加开班信息')

const handleEditButton = ()=>{
  showEdit.value = !showEdit.value
  if(showEdit.value){
    buttonText.value = '保存修改'
  }else{
    buttonText.value = '添加开班信息'
    // 提交修改

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
  adminGetCourseInfo({
    classId:selectClass.value
  }).then(res=>{
    if(res.status===200){
      courseData.value = res.data.data.courseData
    }
  })
}

const onFileError=()=>{
  Message.error("上传失败")
}

const deleteCourse=(classId,courseId)=>{
  deleteCourseInfo({
    classId:classId,
    courseId:courseId
  }).then(res=>{
    if(res.status===200){
      Message.success(res.data.data.msg)
      courseData.value = courseData.value.filter(item=>{
        return item.classId !== classId || item.courseId !== courseId
      })
    }
  })
}
</script>