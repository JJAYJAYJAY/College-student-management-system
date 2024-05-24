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
      :default-selected-keys="[defaultSelectedKeys]"
      :default-open-keys="[defaultSelectedGroup]"
  >
    <a-sub-menu v-for="[groupName,itemGroup] of Object.entries(menuList)" :key="groupName">
      <template #icon>
        <component :is="itemGroup.icon" />
      </template>
      <template #title>{{groupName}}</template>
        <a-menu-item v-for="(item) in itemGroup.menuItem" :key="item.name" :class="['menuItem']" @click="handleClick(item.path)">
          {{item.name}}
        </a-menu-item>
    </a-sub-menu>
  </a-menu>
</template>

<script setup lang="js">

import {useRouter} from "vue-router";
import {ref} from "vue";
const props = defineProps({
  menuList: Object,
})

const defaultSelectedKeys = ref('');
const router = useRouter();
const handleClick = (path) => {
  router.push('/home/'+path);
}


// 读取菜单加路由的字典
let menuPath = {};
for (let [_,itemGroup] of Object.entries(props.menuList)){
  for (let item of itemGroup.menuItem){
    menuPath[item.path] = item.name;
  }
}
// 读取路由
let path = router.currentRoute.value.path;
let pathArr = path.split('/');
console.log(menuPath[pathArr[pathArr.length-1]]);
defaultSelectedKeys.value = menuPath[pathArr[pathArr.length-1]];

// 读取默认展开的组
let defaultSelectedGroup = ref([]);
for (let [groupName, itemGroup] of Object.entries(props.menuList)){
  for (let item of itemGroup.menuItem){
    if (item.path === pathArr[pathArr.length-1]){
      defaultSelectedGroup.value=groupName;
    }
  }
}


</script>