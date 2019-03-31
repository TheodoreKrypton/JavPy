<template>
  <div class="topbar">
    <div style="height: 100%">
      <span style="float: left">
        <img src="../assets/logo.png" alt="logo" style="height: 60px">
      </span>
      
      <span style="float: right">
        <el-button icon="el-icon-setting" circle></el-button>
      </span>
    </div>

    <div v-if="loading" class="loading-bar"></div>
  </div>
</template>

<script>
import Event from "../main.js";

export default {
  name: "topbar",

  data() {
    return {
      loading: false
    };
  },

  created() {
    let that = this;
    Event.$on("begin-loading", () => {
      that.loading = true;
    });
    Event.$on("end-loading", () => {
      that.loading = false;
    });
  }
};
</script>

<style lang="less" scoped>
.topbar{
  box-shadow: 0px 12px 8px -12px #000; border-radius:10px; 
}

.loading-bar {
  animation: loading 2s infinite linear;
  -webkit-animation: loading 2s infinite linear;
  width: 20%;
  height: 2px;
  background: linear-gradient(to right, #e9eef3, #008080, #e9eef3);
}

@keyframes loading {
  0% {
    margin-left: 0%;
    width: 10%;
  }

  10% {
    margin-left: 0%;
    width: 20%;
  }

  90% {
    margin-left: 80%;
    width: 20%;
  }

  100% {
    margin-left: 90%;
    width: 10%;
  }
}
</style>
