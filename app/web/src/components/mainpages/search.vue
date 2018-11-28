<template>
  <div>
    <el-form ref="form" :model="form" :inline="true">
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
        <el-button type="primary" @click="onSearch">Search!</el-button>
        <el-button @click="clear">Clear</el-button>
      </el-form-item>
    </el-form>
    <preview :av="to_be_previewed"></preview>
  </div>
</template>

<script>
    import axios from 'axios';
    import preview from './preview';
    import Event from '../../main.js';

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
                to_be_previewed: null,
                isPreviewLoading: false
            }
        },
        methods: {
            async onSearch(data=null, instance=this) {
                if(data && !(data instanceof MouseEvent)){
                    instance.form.jav_code = data.jav_code;
                    instance.form.actress = data.actress;
                }
                const loading = instance.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });

                let rsp = null;
                if(!instance.form.jav_code && instance.form.actress){
                    await axios.post("http://localhost:8081/search_by_actress", {
                        'actress': instance.form.actress
                    }).then(function(response){
                        rsp = response;

                    }).catch(function (){
                        loading.close();
                        instance.to_be_previewed = "";

                    });
                    return;
                }
                else if(!instance.form.actress && instance.form.jav_code){
                    await axios.post("http://localhost:8081/search_by_code", {
                        'code': instance.form.jav_code,
                    }).then(function(response){
                        rsp = response;

                    }).catch(function (){
                        loading.close();
                        instance.to_be_previewed = "";
                    });
                    return;
                }

                if(rsp.statusCode === 200) {
                    loading.close();
                    if(!rsp.data){
                        instance.to_be_previewed = "";
                    }
                    else{
                        instance.to_be_previewed = rsp.data;
                    }
                }

                else {
                    loading.close();
                    instance.to_be_previewed = "";
                }

            },

            clear() {
                this.form.jav_code = "";
                this.form.actress = "";
            },

            processEvent(){
                let that = this;
                Event.$on('search_jav_by_code', function(data){
                    that.$router.push({'path': '/search'});
                    that.onSearch(data, that);
                });
            }
        },

        mounted: function(){
            this.processEvent();
        }
    }

</script>

<style lang="less" scoped>

</style>
