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
          <h1>学生信息查询</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">
            信息总览
          </h2>
          <a-descriptions style="margin-bottom: 20px" :data="studentTotalData" size="large" bordered />
          <div style="display:flex;width: 100%">
            <chart style="margin-bottom: 20px;" :option="regionChartOption" :size="{width:'50%',height:'300px'}"></chart>
            <chart style="margin-bottom: 20px;" :option="sexChartOption" :size="{width:'50%',height:'300px'}"></chart>
          </div>
          <h2 style="margin-bottom: 20px">学生信息列表</h2>
          <a-table :columns="columns" :data="studentData"  :pagination="{pageSize:13}"></a-table>
        </div>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">

import {onMounted, ref, watch} from "vue";
import Chart from "@/components/Universal/chart.vue";
import emitter from "@/utils/mitt.js";
import {adminGetStudentInfo} from "@/api/admin.js";

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
    }
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
    }
  },
  {
    title: "已修学分",
    dataIndex: "hadCredit",
    key: "hadCredit",
    width: 60,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "平均学分绩点",
    dataIndex: "GPA",
    key: "GPA",
    width: 100,
    align: "center",
    sortable: {
      sortDirections: ['ascend', 'descend']
    }
  }
]);
const studentData = ref([])
const studentTotalData = ref([])

watch(studentData, (newData) => {
  let sexSet = new Set()
  let regionSet = new Set()
  let majorSet = new Set()
  let classSet = new Set()
  for (let i = 0; i < newData.length; i++) {
    sexSet.add(newData[i].sex)
    regionSet.add(newData[i].region)
    majorSet.add(newData[i].majorName)
    classSet.add(newData[i].className)
  }
  sexSet = Array.from(sexSet)
  regionSet = Array.from(regionSet)
  majorSet = Array.from(majorSet)
  classSet = Array.from(classSet)
  columns.value[2].filterable.filters = sexSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
  columns.value[4].filterable.filters = regionSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
  columns.value[5].filterable.filters = majorSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
  columns.value[6].filterable.filters = classSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
})

const regionChartOption = ref({
  title: {
    text: "生源地统计",
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
  adminGetStudentInfo().then(res=>{
    if(res.status===200){
      studentData.value=res.data.data.students
      setTotalData(res.data.data)
      regionChartOption.value = {
        series: [
          {
            type: "pie",
            data: res.data.data.regionData
          }
        ]
      }
      sexChartOption.value = {
        series: [
          {
            type: "pie",
            data: res.data.data.sexData
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
  studentTotalData.value = [
    {
      label: "学生总数",
      value: data.totalData.totalStudent
    },
    {
      label: "总体平均学分绩点",
      value: data.totalData.averageGpa
    }
  ]
}

</script>