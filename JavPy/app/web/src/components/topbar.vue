<template>
  <div class="topbar">
    <span style="float: left; height: 60px">
      <img src="../assets/logo.png" alt="logo" style="height: 60px" />
    </span>

    <span style="float: right">
      <el-popover placement="bottom" width="100" trigger="click">
        <admin style="z-index: 9999"></admin>
        <el-button icon="el-icon-setting" circle slot="reference"></el-button>
      </el-popover>
    </span>

    <div v-if="loading" class="loading-bar"></div>
  </div>
</template>

<script>
import Event from "../main.js";
import admin from "./popups/admin";

export default {
  name: "topbar",
  components: {
    admin
  },
  data() {
    return {
      loading: false,
      gridData: []
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
.topbar {
  box-shadow: 0px 12px 8px -12px #000;
  border-radius: 10px;
}

.loading-bar {
  animation: loading 3s infinite linear;
  -webkit-animation: loading 3s infinite linear;
  width: 20%;
  height: 3px;
  background: linear-gradient(to right, #f2f6fc, #008080, #f2f6fc);
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
