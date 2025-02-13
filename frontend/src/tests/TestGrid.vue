<template>
  <div>
    <div class="grid-container">
      <div v-for="(obj, key) in all_data" :key="key" class="column">
        <div v-for="(item, index) in obj.item_list" :key="index" class="item">
          {{ item }}
        </div>
      </div>
    </div>
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
      all_data: {
        obj1: {item_list: ['Item 1-1', 'Item 1-2', 'Item 1-3']},
        obj2: {item_list: ['Item 2-1', 'Item 2-2']},
        obj3: {item_list: ['Item 3-1', 'Item 3-2', 'Item 3-3', 'Item 3-4']}
      }
    }
  },

  methods: {}
}
</script>
<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); /* 根据需要调整列宽 */
  grid-auto-rows: minmax(50px, auto); /* 根据需要调整行高 */
  gap: 10px; /* 列与列之间的间距 */
}

.column {
  display: contents; /* 使 .column 元素不生成额外的网格区域 */
}

.item {
  background-color: #f0f0f0;
  padding: 10px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
