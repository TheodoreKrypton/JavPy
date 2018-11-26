<template>
  <div>
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="活动名称">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search_by_code">立即创建</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

import axios from 'axios';

export default {
    data() {
      return {
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        }
      }
    },
    methods: {
      search_by_code() {
        const config = {
            'origin': 'localhost:8081'
        }

        axios.get("http://localhost:8081/search", config)
        .then(function(response){
            console.log(response);
        })
        .catch(function(error){
            console.log(error);
        });
      }
    }
  }

</script>

<style lang="less" scoped>

</style>
