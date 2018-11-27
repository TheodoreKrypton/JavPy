<template>
  <div>
    <el-form ref="form" :model="form" :inline="true" @submit="search_by_code">
      <el-form-item>
        <el-input v-model="form.jav_code" placeholder="Jav Code"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input v-model="form.actress" placeholder="Actress"></el-input>
      </el-form-item>
      <el-form-item>
        <el-switch
          v-model="form.allow_many_actresses"
          active-color="#13ce66"
          inactive-color="#ff4949"
        ></el-switch>
      </el-form-item>
      <el-form-item>
        <el-input-number
          v-model="form.up_to"
          controls-position="right"
          :min="1"
          label="Count"
          size="mini"
          style="width: 80px"
        ></el-input-number>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="search_by_code">Search!</el-button>
        <el-button @click="clear">Clear</el-button>
      </el-form-item>
    </el-form>
    <preview :av="to_be_previewed"></preview>
  </div>
</template>

<script>

    import axios from 'axios';
    import preview from './preview';

    export default {
        name: 'search',
        components: {
            preview
        },
        data() {
            return {
                form: {
                    jav_code: '',
                    actress: '',
                    allow_many_actresses: false,
                    up_to: 0
                },
                to_be_previewed: null
            }
        },
        methods: {
            async search_by_code() {
                const data = {
                    'code': this.form.jav_code,
                    'actress': this.form.actress
                };

                const rsp = await axios.post("http://localhost:8081/search", data);
                this.to_be_previewed = rsp.data;
            },

            clear() {
                this.form.jav_code = "";
                this.form.actress = "";
            }
        }
    }

</script>

<style lang="less" scoped>

</style>
