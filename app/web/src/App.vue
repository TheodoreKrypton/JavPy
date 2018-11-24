<template>
  <div id="app">
    <index style="height: 100%;"/>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import index from './components/index.vue'

export default {
  name: 'app',
  components: {
      // HelloWorld,
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
