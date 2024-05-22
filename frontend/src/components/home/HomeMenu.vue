<style scoped>
.menu{
  height: 100%;
  font-size: large;
  background-color: #ffffff;
}
</style>

<template>
  <a-menu
      class="menu"
      @menu-item-click="handleClick"
      :default-selected-keys="['1']"
  >
    <a-sub-menu v-for="[groupName,itemGroup] of Object.entries(menuList)">
      <template #icon>
        <component :is="itemGroup.icon" />
      </template>
      <template #title>{{groupName}}</template>
        <a-menu-item v-for="(item,index) in itemGroup.menuItem" :key="item.key" :class="['menuItem']" @click="handleClick(item.path)">
          {{item.name}}
        </a-menu-item>
    </a-sub-menu>
  </a-menu>
</template>

<script setup lang="js">

import { useRouter } from "vue-router";

const props = defineProps({
  menuList: Object
})

const router = useRouter();
const handleClick = (path) => {
  router.push('/home/'+path);
}

</script>