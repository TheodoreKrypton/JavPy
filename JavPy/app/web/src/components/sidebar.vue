<template>
  <el-row class="tac">
    <el-col
      :span="12"
      style="height: 100%"
    >
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-discover"></i>
            <span>Internet</span>
          </template>
          <el-menu-item
            index="1-1"
            @click="toSearch"
          >Search</el-menu-item>
          <el-menu-item
            index="1-1"
            @click="toNew"
          >New</el-menu-item>
          <el-menu-item
            index="1-2"
            @click="toMagnet"
          >Magnet</el-menu-item>
          <el-menu-item
            index="1-3"
            @click="toCategory"
          >Categories</el-menu-item>
          <el-menu-item
            index="1-4"
            @click="toSeries"
          >Series</el-menu-item>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-s-home"></i>
            <span>Local</span>
          </template>
        </el-submenu>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "sidebar",
  data() {
    return {
      isCollapse: true
    };
  },
  methods: {
    handleOpen(key, keyPath) {},
    handleClose(key, keyPath) {},
    toSearch() {
      this.$router.push({ path: "/search" });
    },
    toNew() {
      this.$router.push({ path: "/new" });
    },
    toMagnet() {
      this.$router.push({ path: "/magnet" });
    },
    toCategory() {
      this.$router.push({ path: "/categories" });
    }
  }
};
</script>

<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 100%;
  margin: 0;
}
</style>
