<template>
  <div>
    <table class="data-table">
      <thead>
      <tr>
        <th v-for="(obj, key) in all_data" :key="key">{{ obj.name }}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(rowIndex, row) in maxItemLength" :key="rowIndex">
        <td v-for="(obj, key) in all_data" :key="key">
          {{ obj.item_list[rowIndex] || '' }}
        </td>
      </tr>
      </tbody>
    </table>

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
        obj1: {
          name: 'Column 1',
          item_list: ['Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3', 'Item 1-1', 'Item 1-2', 'Item 1-3']
        },
        obj2: {name: 'Column 2', item_list: ['Item 2-1', 'Item 2-2']},
        obj3: {name: 'Column 3', item_list: ['Item 3-1', 'Item 3-2', 'Item 3-3', 'Item 3-4']}
      }
    }
  },
  computed: {
    maxItemLength() {
      return Math.max(...Object.values(this.all_data).map(obj => obj.item_list.length));
    }
  },
  methods: {}
}
</script>
<style scoped>

thead th {
  position: sticky;
  top: 0;
  z-index: 1;
}

.data-table {
  width: 100%;
  border-collapse: collapse;

  display: block;
  height: 90vh;
  overflow-y: auto;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.data-table th {
  background-color: #f0f0f0;
  font-weight: bold;
}
</style>
