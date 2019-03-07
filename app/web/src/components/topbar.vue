<template>
  <div>
    <div>
      <span style="float: left">
        <img src="../assets/logo.png" alt="logo" style="height: 60px">
      </span>
      
      <span style="float: right">
        <el-button icon="el-icon-setting" circle></el-button>
      </span>
    </div>
    <div class="loading-bar"></div>
  </div>
</template>

<script>

</script>

<style lang="less" scoped>
  .loading-bar{
      animation: loading 2s infinite linear;
      -webkit-animation: loading 2s infinite linear;
  
      width: 20%;
      height: 3px;
      bottom: 0;
      background: linear-gradient(to right, #E9EEF3, #008080, #E9EEF3);
  }

  @keyframes loading{
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
