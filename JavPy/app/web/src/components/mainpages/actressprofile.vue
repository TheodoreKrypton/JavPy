<template>
  <div>
    <el-row>
      <el-col :span="12">
        <img style="max-height: 200px" :src="info.img" />
      </el-col>
      <el-col :span="12">
        <h1>{{name}}</h1>
        <ul v-if="info" style="text-align: left">
          <li>Birthdate: {{info.birth_date}}</li>
          <li>Height: {{info.height}}</li>
          <li>Weight: {{info.weight}}</li>
        </ul>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  props: ["name", "info"]
};
</script>

<style scoped>
</style>