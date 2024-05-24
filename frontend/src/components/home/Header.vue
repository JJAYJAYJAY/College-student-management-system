<template>
  <div class="header">
    <a-page-header
        :style="{ background: 'var(--color-bg-2)',height:'100%',}"
        class="header"
        @back="back"
        :show-back="router.currentRoute.value.name !== 'Home'"
    >
      <template #title>
        <span style="font-size: xx-large">&emsp;浙江工业大学&emsp;</span>
      </template>
      <template #subtitle>
        <span style="font-size: large">高校成绩管理系统</span>
      </template>
      <template #back-icon>
        <icon-left style="transform: scale(1.2)"/>
      </template>
    </a-page-header>
  </div>
</template>

<script setup lang="js">
import {useRouter} from "vue-router";
import {Icon} from "@arco-design/web-vue";

const router=useRouter();

const back = () => {
  router.push('/')
  localStorage.removeItem('token');
}

</script>

<style scoped>
.header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 9vh;
  border-bottom: 1px solid var(--color-border);
}

.right-aligned-button{
  margin-right: 5vh;
}
</style>
