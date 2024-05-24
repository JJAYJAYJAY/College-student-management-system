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
      filters: [
        {
          text: "考试",
          value: "考试"
        },
        {
          text: "考查",
          value: "考查"
        }
      ],
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
      filters: [
        {
          text: "2",
          value: 2
        },
        {
          text: "4",
          value: 4
        }
      ],
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
      filters: [
        {
          text: "32",
          value: 32
        },
        {
          text: "64",
          value: 64
        }
      ],
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
      filters: [
        {
          text: "2022-2023上",
          value: "2022-2023上"
        },
        {
          text: "2022-2023下",
          value: "2022-2023下"
        },
        {
          text: "2023-2024上",
          value: "2023-2024上"
        },
        {
          text: "2023-2024下",
          value: "2023-2024下"
        },
        {
          text: "2024-2025上",
          value: "2024-2025上"
        },
        {
          text: "2024-2025下",
          value: "2024-2025下"
        },
        {
          text: "2025-2026上",
          value: "2025-2026上"
        }
      ],
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
  console.log(columns.value[4].filterable.filters)
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
scoreData.value=[
  {
    courseName: "高等数学",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2022-2023上",
    grade: 96,
    point: 4.6
  },
  {
    courseName: "线性代数",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2022-2023下",
    grade: 83,
    point: 3.6
  },
  {
    courseName: "大学英语",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2022-2023上",
    grade: 72,
    point: 2.6
  },
  {
    courseName: "大学体育",
    testMethod: "考试",
    credit: 2,
    hour: 32,
    term: "2022-2023下",
    grade: 61,
    point: 1.6
  },
  {
    courseName: "大学物理",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2022-2023上",
    grade: 56,
    point: 1.6
  },
  {
    courseName: "计算机网络原理",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2023-2024上",
    grade: 78,
    point: 3.6
  },
  {
    courseName: "数据库原理",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2023-2024下",
    grade: 89,
    point: 4.0
  },
  {
    courseName: "数据结构",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2023-2024上",
    grade: 92,
    point: 4.3
  },
  {
    courseName: "操作系统",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2023-2024下",
    grade: 85,
    point: 3.9
  },
  {
    courseName: "编译原理",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2024-2025上",
    grade: 77,
    point: 3.6
  },
  {
    courseName: "软件工程",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2024-2025下",
    grade: 88,
    point: 4.0
  },
  {
    courseName: "人工智能",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2024-2025上",
    grade: 91,
    point: 4.3
  },
  {
    courseName: "大数据",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2024-2025下",
    grade: 93,
    point: 4.3
  },
  {
    courseName: "物联网",
    testMethod: "考试",
    credit: 4,
    hour: 64,
    term: "2025-2026上",
    grade: 94,
    point: 4.6
  }
]

const scoreTotalData = ref([
  {
    label: "总学分",
    value: 56
  },
  {
    label: "总学时",
    value: 896
  },
  {
    label: "总GPA",
    value: 3.6
  }
])
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
    type: "value"
  },
  series: [
    {
      name: "gpa",
      type: "line",
      data: '',
    }
  ]
})

chartOption.value.series[0].data = [
  [
    "2022-2023上",
     3.6
  ],
  [
    "2022-2023下",
     2.6
  ],
  [
    "2023-2024上",
     3.6
  ],
  [
    "2023-2024下",
     3.8
  ],
  [
    "2024-2025上",
     4.1
  ],
  [
    "2024-2025下",
     4.6
  ],
  [
    "2025-2026上",
     3.6
  ]
]

onMounted(()=>{
  setTimeout(()=>{
    emitter.emit('resize')
  },500)

})
</script>