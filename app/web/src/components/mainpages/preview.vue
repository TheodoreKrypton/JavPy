<template>
  <div>
    <el-card v-for="(video, i) in av" :key="i" style="width: 20%;" :body-style="{ padding: '0px' }" shadow="hover">
      <img :src="video.preview_img_url" class="image" alt="preview">
        <div class="bottom">
          <table>
            <tr>
              <td style="width: 70%; text-align: left">
                {{video.code}}
              </td>
              <td>
                <el-button type="primary" plain style="float: right;">主要按钮</el-button>
              </td>
            </tr>
          </table>
        </div>
    </el-card>
  </div>
</template>


<script>
export default {
    name: 'preview',
    props: [
        'av'
    ]
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
