<style scoped>
.login-box{
  width: 800px;
  height: 400px;
  position: absolute;
  left: calc(50% - 400px);
  top:calc(50% - 200px);
  display: flex;
  background: #fff;
  padding: 10px;
  border-radius: 20px;
  filter: drop-shadow(0 0 20px #7a7a7a);
}
.login-photo{
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-photo img{
  object-fit: cover;
  transform: scale(0.55);
}
.right{
  width: 50%;
  height: 100%;
}
.right h1{
  margin-top: 30px;
  font-size: xx-large;
  font-weight: 600;
}
.right h2{
  font-size: x-large;
  font-weight: 600;
  margin-top: 20px;
}
.input-box{
  border: #ccc solid 1px;
  width: 80%;
  display: flex;
  align-items: center;
  margin-top: 30px;
  border-radius: 5px;
  padding: 5px 0;
}
.input-box span{
  padding: 5px;
  font-size:small;
  color: rgb(95, 182, 224);
  font-weight: 600;
  width: 20%;
  text-align: center;
}
.input-box input{
  border: none;
  width: 90%;
  outline: none;
  height: 34px;
  cursor: text;
}
.login-button{
  margin-top:25px ;
  width: 150px;
  height: 50px;
  background-color: #1196fd;
  border: none;
  outline: none;
  border-radius:10px ;
  color: white;
  font-size: large;
  cursor: pointer;
}
</style>

<template>
  <form class="login-box" method="post">
    <div class="login-photo">
      <img src="../../../public/login.png" alt="加载失败">
    </div>
    <div class="right">
      <h1>高校成绩管理系统</h1>
      <h2>你好，欢迎！</h2>
      <div class="input-box">
        <span class="input-label">用户名</span>
        <input type="text" placeholder="请输入用户名" name="username" id="username" v-model="form.username">
      </div>
      <div class="input-box">
        <span class="input-label">密码</span>
        <input  type="password" placeholder="请输入密码" name="password" id="password" v-model="form.password">
      </div>
      <button class="login-button" @click="handleSubmit($event)">登录</button>
    </div>
  </form>
</template>

<script setup lang="js">
import {reactive} from "vue";
import {useRouter} from "vue-router";
import {login} from "@/api/user.js";
import useUserStore from "@/stores/userStore.js";
import {Message} from "@arco-design/web-vue";

let form= reactive({
  username: "",
  password: ""
})

const router= useRouter();

const userStore = useUserStore();

const handleSubmit = (e)=>{
  e.preventDefault();
  // 转跳并传参
  login(form).then(res=>{
    if (res.status === 200){
        localStorage.setItem('token',res.data.data.token);
        switch (res.data.data.role){
        case 0:
          userStore.setRole('student');
          useUserStore().setClassId(res.data.data.classId);
          router.push({path: '/home/studentProfile'});
          break;
        case 1:
          userStore.setRole('teacher');
          router.push({path: '/home/teacherProfile'});
          break;
        case 2:
          userStore.setRole('admin');
          router.push({path: '/home/adminProfile'});
          break;
      }
    }
  }).catch((res)=>{
    if(res.status === 400)
      Message.error('登录失败，请检查用户名和密码');
    else
      Message.error('服务器错误，请稍后再试');
  })
}
</script>