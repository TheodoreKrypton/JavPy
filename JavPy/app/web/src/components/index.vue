<template>
  <div style="height: 100%; position:relative; width:100%;">
    <el-container style="height: 100%">
      <el-header
        style="background: #F2F6FC; position:fixed; margin-top:0; width:100%; z-index:9998; box-shadow: 0 1px 6px 0 rgba(32,33,36,20);"
      >
        <topbar></topbar>
      </el-header>
      <el-container>
        <sidebar style="margin-top: 60px; position: fixed; height: 100%"></sidebar>
        <el-container>
          <el-main style="margin-top: 60px; margin-left: 200px;">
            <div style="position:fixed; bottom:10vmin; right: 1vmin;">
              <el-button
                type="primary"
                icon="el-icon-caret-top"
                style="display:block; margin: 5px;"
                circle
                @click="backToTop()"
              />
              <el-button
                type="primary"
                icon="el-icon-arrow-up"
                style="display:block; margin: 5px;"
                circle
                @click="prev()"
              />
              <el-button
                type="primary"
                icon="el-icon-arrow-down"
                style="display:block; margin: 5px;"
                circle
                @click="next()"
              />
            </div>
            <router-view style="height: 100%;"></router-view>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
    <login></login>
  </div>
</template>

<script>
import sidebar from "./sidebar.vue";
import topbar from "./topbar.vue";
import login from "./popups/login.vue";

export default {
  name: "index",
  components: {
    sidebar,
    topbar,
    login
  },
  methods: {
    backToTop() {
      document.body.scrollTop = document.documentElement.scrollTop = 0;
    },
    prev() {
      const windowHeight = document.documentElement.clientHeight;
      const nextLoc = document.documentElement.scrollTop - windowHeight;
      document.body.scrollTop = document.documentElement.scrollTop =
        nextLoc > 0 ? nextLoc : 0;
    },
    next() {
      const windowHeight = document.documentElement.clientHeight;
      const bottom = document.documentElement.scrollTop + windowHeight;
      const nextLoc = document.documentElement.scrollTop + windowHeight;
      document.body.scrollTop = document.documentElement.scrollTop =
        nextLoc < bottom ? nextLoc : bottom;
    }
  }
};
</script>

<style lang="less" scoped>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
  .element::-webkit-scrollbar {
    width: 0 !important;
  }
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
</style>
