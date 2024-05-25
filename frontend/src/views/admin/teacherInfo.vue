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
          <h1>教师信息查询</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">
            信息总览
          </h2>
          <a-descriptions style="margin-bottom: 20px" :data="teacherTotalData" size="large" bordered />
          <div style="display:flex;width: 100%">
            <chart style="margin-bottom: 20px;" :option="titleChartOption" :size="{width:'50%',height:'300px'}"></chart>
            <chart style="margin-bottom: 20px;" :option="sexChartOption" :size="{width:'50%',height:'300px'}"></chart>
          </div>
          <h2 style="margin-bottom: 20px">教师信息列表</h2>
          <a-table :columns="columns" :data="teacherData" :pagination="{pageSize:13}"></a-table>
        </div>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">

import {onMounted, ref, watch} from "vue";
import Chart from "@/components/Universal/chart.vue";
import emitter from "@/utils/mitt.js";
import {adminGetTeacherInfo} from "@/api/admin.js";

const columns = ref([
  {
    title: "教师号",
    dataIndex: "teacherId",
    key: "teacherId",
    width: 120,
    align: "center"
  },
  {
    title: "姓名",
    dataIndex: "teacherName",
    key: "teacherName",
    width: 70,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
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
    }
  },
  {
    title: "年龄",
    dataIndex: "age",
    key: "age",
    width: 50,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "职称",
    dataIndex: "jobTitle",
    key: "jobTitle",
    width: 50,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    },
    filterable: {
      filters: [],
      multiple: true,
      filter:(value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.jobTitle === value[i]) {
            return true
          }
        }
      },
    }
  },
  {
    title: "手机号",
    dataIndex: "phone",
    key: "phone",
    width: 150,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
]);
const teacherData = ref([])
const teacherTotalData = ref([])

watch(teacherData, (newData) => {
  let sexSet = new Set()
  let jobTitleSet = new Set()
  for (let i = 0; i < newData.length; i++) {
    sexSet.add(newData[i].sex)
    jobTitleSet.add(newData[i].jobTitle)
  }
  let sexArray = Array.from(sexSet)
  let jobTitleArray = Array.from(jobTitleSet)
  columns.value[2].filterable.filters = sexArray.map(item => {
    return {text: item, value: item}
  })
  columns.value[4].filterable.filters = jobTitleArray.map(item => {
    return {text: item, value: item}
  })
})

const titleChartOption = ref({
  title: {
    text: "职称统计",
    left: "center"
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: "vertical",
    left:"30px"
  },
  series: [
    {
      type: "pie",
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      padAngle: 5,
      itemStyle: {
        borderRadius: 10
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      data: []
    }
  ]
})

const sexChartOption = ref({
  title: {
    text: "性别统计",
    left: "center"
  },
  tooltip: {
    trigger: "item"
  },
  legend: {
    orient: "vertical",
    left:"30px"
  },
  series: [
    {
      type: "pie",
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      padAngle: 5,
      itemStyle: {
        borderRadius: 10
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      data: []
    }
  ]
})

onMounted(()=>{
  adminGetTeacherInfo().then(res=>{
    if(res.status===200){
      teacherData.value=res.data.data.teachers
      setTotalData(res.data.data)
      titleChartOption.value = {
        series: [
          {
            data:res.data.data.jobTitleData
          }
        ]
      }
      sexChartOption.value = {
        series: [
          {
            data:res.data.data.sexData
          }
        ]
      }
    }
  })
  setTimeout(()=>{
    emitter.emit('resize')
  },500)
})

const setTotalData = (data) => {
  teacherTotalData.value = [
    {
      label: "教师总数",
      value: data.totalData.totalTeacher
    },
    {
      label: "教师平均年龄",
      value: data.totalData.averageAge
    }
  ]
}

</script>