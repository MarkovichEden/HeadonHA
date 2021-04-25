<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  apiUrl: 'http://10.100.102.13:5000/api/v1',
  components: {
  },

  destroyed() {
    localStorage.clear()
  },

  data: () => ({
    
  }),
};
</script>

<style>
.link {
  color: whitesmoke;
}
</style>