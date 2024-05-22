<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body{
  height: 100%;
  width: 100%;
}
html{
  min-width: 1450px;
  height: 100%;
}
textarea{
  resize: none !important;
}
</style>
