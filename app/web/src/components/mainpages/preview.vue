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
                <showcard :video=video></showcard>
            </el-col>
        </el-row>
    </div>
</template>


<script>
import showcard from './showcard.vue'

export default {
    name: 'preview',
    components: {
        showcard
    },
    props: [
        'av'
    ]
}
</script>


<style lang="less" scoped>

</style>
