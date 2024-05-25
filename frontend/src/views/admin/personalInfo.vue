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
import {getAdminInfo} from "@/api/admin.js";

const studentData=ref([])

const CHINESE_DICT = {
  'adminId': '管理员账号',
  'adminName': '姓名'
}
onMounted(()=>{
  getAdminInfo().then(res=>{
    if(res.status===200){
      studentData.value=Object.keys(res.data.data).map(key=>{
        return {
          label: CHINESE_DICT[key],
          value: res.data.data[key]
        }
      })
    }
  })
})
</script>