<template>
  <div class="home">
  </div>
</template>

<script>
// @ is an alias to /src
import router from "@/router"

export default {
  name: 'Home',
  components: {
  },

  created() {
    if(localStorage.getItem("token") !== null) {
      router.push("Dashboard")
    } else {
      router.push("Login")
    }
  },
}
</script>

<style>

.home {
  height: 100%;
}
</style>
