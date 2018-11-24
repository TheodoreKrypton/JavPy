<template>
    <div style="height: 100%">
        <el-container style="height: 100%">
            <el-header>Header</el-header>
            <el-container>
                <sidebar/>
                <el-container>
                    <el-main>Main</el-main>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>

<script>
    import sidebar from './sidebar.vue'
    export default {
        name: 'index',
        components: {
            sidebar
        }
    }
</script>

<style lang="less" scoped>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        text-align: center;
        line-height: 60px;
    }

    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 200px;
        .element::-webkit-scrollbar { width: 0 !important }
    }

    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 160px;
    }

    .el-container:nth-child(5) .el-aside,
    .el-container:nth-child(6) .el-aside {
        line-height: 260px;
    }

    .el-container:nth-child(7) .el-aside {
        line-height: 320px;
    }
</style>
