<template>
  <div>
    <table class="data-table" v-if="maxItemLength>0">
      <thead>
      <tr>
        <th v-for="(obj, key) in all_data" :key="key">

          <div class="column_name">
            <i class="el-icon-close" @click="$emit('close_folder',obj)"></i>
            <span> {{ obj.custom_name || obj.name }}</span>
            <i class="el-icon-edit" @click="$emit('edit_folder',obj)"></i>
          </div>
          <div class="column_info">
            {{ formatKVDict(obj.info) }}
          </div>


        </th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="rowIndex  in indexArray" :key="rowIndex">
        <td v-for="(obj, key) in all_data" :key="key">
          <div v-if="obj.items[rowIndex]">
            <div class="item_name">
              <span style="color: #42b983">【{{ rowIndex }}】</span>
              {{ obj.items[rowIndex].name }}
              <i class="el-icon-edit" @click="onEditHtml(obj,rowIndex)"></i>
            </div>
            <div class="item_text" v-html="obj.name2text[obj.items[rowIndex].name]"></div>

            <LazyAudio :path="obj.items[rowIndex].path"></LazyAudio>
            <div class="item_info">{{ formatKVDict(obj.items[rowIndex].info) }}</div>
          </div>
        </td>
      </tr>
      </tbody>
    </table>

    <TextEditorDialog ref="TextEditorDialog"/>

  </div>
</template>

<script>

import LazyAudio from "@/components/LazyAudio.vue";
import format_util from "@/utils/format_util.js";
import TextEditorDialog from "@/components/TextEditorDialog.vue";
import web_util from "@/utils/web_util";

export default {
  name: 'MyTableView',
  components: {LazyAudio, TextEditorDialog},
  props: ['all_data'],
  data() {
    return {
      // all_data: []
    }
  },
  computed: {

    maxItemLength() {
      try {
        return Math.max(...this.all_data.map(obj => obj.items.length));
      } catch (e) {
        return 0
      }
    },
    indexArray() {
      // 直接v-for遍历maxItemLength，下标是从1开始的，为此，直接遍历这个数组
      // 生成从 0 到 maxItemLength - 1 的数组
      return Array.from({length: this.maxItemLength}, (_, i) => i);
    },
  },
  mounted() {

    // this.all_data = [
    //   {
    //     name: 'Column 1',
    //     item_list: ['Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3']
    //   },
    //   {name: 'Column 2', item_list: ['Item 2-1', 'Item 2-2']},
    //   {name: 'Column 3', item_list: ['Item 3-1', 'Item 3-2', 'Item 3-3', 'Item 3-4']}
    // ]
    //
  },
  methods: {
    formatKVDict: format_util.formatKVDict,
    async onEditHtml(obj, rowIndex) {
      const text = obj.name2text[obj.items[rowIndex].name]
      const newText = await this.$refs.TextEditorDialog.editHtml(text)
      obj.name2text[obj.items[rowIndex].name] = newText
      await web_util.getHttp().post("/update_name2text", {'path': obj.path, 'name2text': obj.name2text})
      this.$message.success("保存成功")
    }
  }
}
</script>
<style scoped>
.column_name > i:hover {
  color: red;
  margin-left: 2px;
}

.item_name {
  font-size: xx-small;
  width: 100%; /* 或者你可以设置一个固定宽度 */
  /*white-space: nowrap; !* 确保文本在一行内显示 *!*/
  /*overflow: hidden; !* 隐藏超出部分 *!*/
  /*text-overflow: ellipsis; !* 当文本被截断时显示省略号 *!*/
  color: gray;
}

.item_text {
  text-align: left;
  font-size: 0.8rem;
}

.item_info {
  font-size: small;
}

.column_info {
  font-size: small;
  font-weight: lighter;
}

.column_name {
  font-size: xx-small;
  font-weight: bold;
  width: 100%; /* 或者你可以设置一个固定宽度 */
  white-space: nowrap; /* 确保文本在一行内显示 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 当文本被截断时显示省略号 */
}


thead th {
  position: sticky;
  top: 0;
  z-index: 1;
}

.data-table {
  width: 100%;
  max-width: 100%;
  border-collapse: collapse;

  display: block;
  height: calc(100vh - 100px);
  overflow: auto;
}

.data-table th,
.data-table td {
  /*border: 1px solid #ddd;*/
  border: none;
  padding: 10px 5px;
  text-align: center;

  /*这里我限制了最大宽度*/
  max-width: 40vw;
}

.data-table th {
  background-color: #f0f0f0;
  font-weight: bold;
}
</style>
