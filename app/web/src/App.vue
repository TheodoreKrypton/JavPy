<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import index from './components/index.vue'

export default {
  name: 'app',
  components: {
      index
  }
}
</script>

<style>
html {
  margin: 0;
  height: 100%;
}
body {
  margin: 0;
  height: 100%;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
  height: 100%;
}
</style>
