<template>
  <div>
    <quill-editor
        v-model="content"
        :options="editorOption"
    ></quill-editor>

    <div>{{content}}</div>
  </div>
</template>

<script>
import web_util from "@/utils/web_util";


export default {
  name: 'Empty',
  components: {},
  props: [],
  data() {
    return {
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
  methods: {}
}
</script>
<style scoped>

</style>
