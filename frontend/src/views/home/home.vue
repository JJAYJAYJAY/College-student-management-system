<style scoped>
.Menu {
  height: 100%;
}

.sider{
  padding:20px 0 20px 20px;
}
.mainContent{
  display: flex;
  align-items: center;
  padding: 30px;
  height: 91vh;
}

</style>

<template>
  <a-layout class="container">
    <a-layout-header>
      <Header />
    </a-layout-header>
    <a-layout-content>
      <a-layout style="background: #f2f3f5;" >
        <a-layout-sider class="sider" :width="250">
          <HomeMenu class="Menu" :menu-list="menuList"/>
        </a-layout-sider>
        <a-layout-content class="mainContent">
          <RouterView style="height: 100%;width: 100%"/>
        </a-layout-content>
      </a-layout>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="js">
import Header from "@/components/home/Header.vue";
import HomeMenu from "@/components/home/HomeMenu.vue";
import {ref} from "vue";
import {RouterView} from "vue-router";
import {MENU} from "@/constant/homeConfig.js";
import {useRouter} from "vue-router";
import useUserStore from "@/stores/userStore.js";

const menuList=ref({})


const router = useRouter();
//获取get参数
const role = useUserStore().user.role
menuList.value=MENU[role]
</script>