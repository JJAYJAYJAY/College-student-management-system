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
          <h1>成绩查询</h1>
          <a-descriptions bordered />
        </a-col>
        <div class="content">
          <h2 style="margin-bottom: 20px">
            成绩总评
          </h2>
          <a-descriptions style="margin-bottom: 20px" :data="scoreTotalData" size="large" bordered />
          <chart style="margin-bottom: 20px;" :option="chartOption" :size="{width:'100%',height:'300px'}"></chart>
          <h2 style="margin-bottom: 20px">成绩详情</h2>
          <a-table :columns="columns" :data="scoreData"  :pagination="{pageSize:13}"></a-table>
        </div>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">

import {onMounted, ref, watch} from "vue";
import Chart from "@/components/Universal/chart.vue";
import emitter from "@/utils/mitt.js";
import {getStudentGrade} from "@/api/student.js";

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
      filter:(value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.testMethod.includes(value[i])) {
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
      filter:(value, record) => {
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
    dataIndex: "hour",
    key: "hour",
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
          if (record.hour === value[i]) {
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
      filter:(value, record) => {
        for (let i = 0; i < value.length; i++) {
          if (record.term.includes(value[i])) {
            return true
          }
        }
      },
    },
  },
  {
    title: "成绩",
    dataIndex: "grade",
    key: "grade",
    width: 100,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  },
  {
    title: "绩点",
    dataIndex: "point",
    key: "point",
    width: 100,
    align: "center",
    sortable:{
      sortDirections: ['ascend', 'descend']
    }
  }
]);
const scoreData = ref([])
scoreData.value=[]
const scoreTotalData = ref([])

watch(scoreData, (newData) => {
  //统计学期类型
  let termSet = new Set()
  for (let i = 0; i < newData.length; i++) {
    termSet.add(newData[i].term)
  }
  termSet = Array.from(termSet)
  columns.value[4].filterable.filters = termSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
  //统计学分类型
  let creditSet = new Set()
  for (let i = 0; i < newData.length; i++) {
    creditSet.add(newData[i].credit)
  }
  creditSet = Array.from(creditSet)
  columns.value[2].filterable.filters = creditSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
  //统计考察方式类型
  let testMethodSet = new Set()
  for (let i = 0; i < newData.length; i++) {
    testMethodSet.add(newData[i].testMethod)
  }
  testMethodSet = Array.from(testMethodSet)
  columns.value[1].filterable.filters = testMethodSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
  //统计学时
  let hourSet = new Set()
  for (let i = 0; i < newData.length; i++) {
    hourSet.add(newData[i].hour)
  }
  hourSet = Array.from(hourSet)
  columns.value[3].filterable.filters = hourSet.map((item) => {
    return {
      text: item,
      value: item
    }
  })
})

const chartOption = ref({
  title: {
    text: "历学期gpa统计",
    left: "center"
  },
  tooltip: {
    trigger: "axis"
  },
  legend: {
    data: ["gpa"],
    bottom: 6
  },
  xAxis: {
    type: "category"
  },
  yAxis: {
    type: "value",
    min:function (value) {
      return value.min - 0.2
    },
    max:function (value) {
      return value.max + 0.1
    }
  },
  series: [
    {
      name: "gpa",
      type: "line",
      data: [],
    }
  ]
})

onMounted(()=>{
  getStudentGrade().then(res=>{
    if (res.status === 200){
      let data = res.data.data
      setTotalData(data)
      setTermGPA(data)
      setDetailData(data)
    }
  })
  setTimeout(()=>{
    emitter.emit('resize')
  },500)
})

const setTotalData = (data) => {
  scoreTotalData.value = [
    {
      label: "总学分",
      value: data.hadCredit
    },
    {
      label: "总学时",
      value: data.totalHours
    },
    {
      label: "总GPA",
      //保留两位小数
      value: Number(data.GPA).toFixed(3)
    }
  ]
}
const setTermGPA = (data) => {
  let termGPA = []
  for (let i = 0; i < data.termGpa.length; i++) {
    termGPA.push([
        data.termGpa[i].term,
        Number(Number(data.termGpa[i].GPA).toFixed(3))
    ])
  }
  chartOption.value={
    series:[
      {
        data: termGPA
      }
    ]
  }
}

const setDetailData = (data) => {
  scoreData.value = data.courseGrade.map((item) => {
    return {
      courseName: item.courseName,
      testMethod: item.testMethod,
      credit: item.credit,
      hour: item.hours,
      term: item.term,
      grade: item.grade,
      point: Number(item.point).toFixed(1)
    }
  })
}
</script>