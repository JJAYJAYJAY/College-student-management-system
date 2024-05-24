<style scoped>

</style>

<template>
  <div>
    <a-space direction="vertical" style="width: 100%;">
      <a-row :gutter="80">
        <a-col :span="16">
          <a-descriptions :data="studentData" size="large" title="个人信息" :column="1"/>
        </a-col>
      </a-row>
    </a-space>
  </div>
</template>

<script setup lang="js">
import {onMounted, ref} from "vue";

const studentData=ref([])
onMounted(()=>{
  studentData.value=[
    {
      label: '姓名',
      value: '张三'
    },
    {
      label: '学号',
      value: '2018000000'
    },
    {
      label: '性别',
      value: '男'
    },
    {
      label: '专业',
      value: '软件工程'
    },
    {
      label: '班级',
      value: '软件1801'
    },
    {
      label: '生源地',
      value: '宁波'
    }
  ]
})
</script>