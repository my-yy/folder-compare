<template>
  <el-dialog title="Collection" :visible.sync="dialogVisible" width="70%" :close-on-click-modal="false">
    <div>
      <quill-editor
          v-model="content"
          :options="editorOption"
      ></quill-editor>

      <!--      <div>{{ content }}</div>-->
      <div style="text-align: center">
        <el-button @click="onSave">Save</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>


import web_util from "@/utils/web_util";

export default {
  name: 'TextEditorDialog',
  components: {},
  props: [],
  data() {
    return {
      dialogVisible: false,
      content: '', // 绑定的富文本内容
      editorOption: {
        modules: {
          toolbar: [
            ['bold', 'italic', 'underline', 'strike'], // 格式化工具
            [{color: []}, {background: []}], // 文字颜色和背景颜色
            [{align: []}], // 对齐方式
            ['clean'], // 清除格式
          ],
        },
      },
    }
  },
  mounted() {
    this.content = "你好哇"
  },
  methods: {
    editHtml(content) {
      this.content = content
      this.dialogVisible = true
      return new Promise(((resolve, reject) => {
        this.resolve = resolve
      }))
    },
    async onSave() {
      this.$message.success("保存成功")
      this.dialogVisible = false
      this.resolve(this.content)
    }
  }
}
</script>
<style scoped>

</style>
