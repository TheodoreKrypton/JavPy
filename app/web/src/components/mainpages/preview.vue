<template>
    <div style="text-align: center">
        <el-alert v-if="av === ''"
                title="Sorry, cannot find any result."
                type="error"
                description="Please Retry."
                show-icon>
        </el-alert>
        <el-row :gutter="40">
            <el-col :span="6" v-for="(video, i) in av" :key="i" :offset="1"
                    style="margin: 0; margin-bottom: 40px;">
                <el-card :body-style="{ padding: '0px' }" shadow="hover">
                    <img :src="video.preview_img_url" class="image" alt="preview">
                    <div class="bottom">
                        <table>
                            <tr>
                                <td style="width: 70%; text-align: left">
                                    {{video.code}}
                                </td>
                                <td v-if="video.video_url">
                                    <el-button type="primary" plain style="float: right;" @click="onWatch(video.video_url)">Watch</el-button>
                                </td>
                                <td v-else>
                                    <el-button type="primary" plain style="float: right;" @click="onSearch(video.code)">Search</el-button>
                                </td>
                            </tr>
                        </table>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>


<script>
    import Event from "../../main.js"

    export default {
        name: 'preview',
        props: [
            'av',
            'brief'
        ],
        methods:{
            onWatch(url){
                window.open(url);
            },
            onSearch(code){
                Event.$emit('search_jav_by_code', {jav_code: code});
            }
        }
    }
</script>

<style lang="less" scoped>
    .bottom {
        margin-top: 10px;
        line-height: 12px;
    }

    .image {
        width: 100%;
        display: block;
    }
</style>
