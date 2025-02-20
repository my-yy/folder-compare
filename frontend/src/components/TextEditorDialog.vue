<template>
  <el-dialog title="TextEdit" :visible.sync="dialogVisible" width="70%" :close-on-click-modal="false">
    <div>
      <quill-editor
          v-model="content"
          :options="editorOption"
      ></quill-editor>
      <div style="text-align: center;margin-top: 10px;">
        <el-button @click="onSave">Save</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>

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
    // this.content = "你好哇"
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
      this.dialogVisible = false
      this.resolve(this.content)
    }
  }
}
</script>
<style scoped>

</style>
