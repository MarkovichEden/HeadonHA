<template>
  <div class="login">
    <AppBar links="links"/>
    <LoginComponent />
  </div>
</template>


<script>
import LoginComponent from "@/components/Login.vue";
import AppBar from "@/components/AppBar.vue"

export default {
  name: 'Login',
  components: {
    AppBar,
    LoginComponent,
  },
  data() {
    links: [
      {
        to: "/",
        text: "Home"
      }
    ]
  }
}
</script>