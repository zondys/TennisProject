<template>
  <the-navbar></the-navbar>
  <div className="container with-nav">
    <app-message></app-message>
    <router-view></router-view>
  </div>
</template>

<script>
import TheNavbar from "@/components/TheNavbar";
import AppMessage from "@/components/ui/AppMessage";

export default {
  name: "MainLayout",
  components: {AppMessage, TheNavbar}
}
</script>

<style scoped>

</style>