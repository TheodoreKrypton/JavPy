<template>
    <preview :av="to_be_previewed"></preview>
</template>

<script>
    import preview from "./preview";
    import axios from 'axios';

    export default {
        name: 'newly_released',
        components: {
            preview
        },
        data(){
            return {
                to_be_previewed: null
            }
        },

        created: async function () {
            const data = {

            };
            const rsp = await axios.post("http://mornlngstar.co:8081/new", data);
            if(!rsp.data){
                this.to_be_previewed = "";
            }
            else{
                this.to_be_previewed = rsp.data;
            }
        }
    }
</script>

<style lang="less" scoped>


</style>
