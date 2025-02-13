<template>
  <el-dialog title="Collection" :visible.sync="dialogVisible" width="70%">
    <div>
      <el-form label-width="100px">
        <el-form-item label="Orders">
          <div>
            <!--            <div v-for="col in column_list">-->
            <!--              {{ col.custom_name }}-->
            <!--            </div>-->
            <!--            <draggable v-model="column_list" @end="onEnd">-->
            <!--              <template #item="{ element }">-->
            <!--                <div class="draggable-item">-->
            <!--                  {{ element.custom_name }}-->
            <!--                </div>-->
            <!--              </template>-->
            <!--            </draggable>-->

            <draggable v-model="column_list" group="people">
              <span class="the_drag_item" v-for="element in column_list" :key="element.id">{{
                  element.custom_name
                }}</span>
            </draggable>
            <!--            <div>{{column_list}}</div>-->

          </div>
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="collection.name"></el-input>
        </el-form-item>
        <el-form-item label="Desc">
          <el-input v-model="collection.desc" type="textarea"></el-input>
        </el-form-item>
        <el-form-item label="Raw">
          <el-input v-model="collection.raw_folders" type="textarea" :rows="5"></el-input>
        </el-form-item>
      </el-form>
    </div>

    <div style="text-align: center;">
      <el-button type="primary" @click="onSave">确 定</el-button>
    </div>

  </el-dialog>
</template>

<script>
import web_util from "@/utils/web_util";
import draggable from 'vuedraggable'

export default {
  name: 'CollectionDialog',
  components: {
    draggable
  },
  props: [],
  data() {
    return {
      dialogVisible: false,
      collection: {
        name: "",
        desc: "",
      },
      resolve: null,
      column_list: []
    }
  },
  mounted() {

  },
  methods: {
    onEnd() {
      console.log('拖拽结束');
    },
    newCollection(column_list, raw_folders = "") {
      const ids = column_list.map(item => item.id)
      this.column_list = column_list.map(obj => {
        return {
          custom_name: obj.custom_name,
          id: obj.id
        }
      })

      this.collection = {
        name: "",
        desc: "",
        ids: ids,
        raw_folders: raw_folders
      }
      this.dialogVisible = true
      return new Promise(((resolve, reject) => {
        this.resolve = resolve
      }))
    },
    updateCollection(collection, column_list) {
      this.collection = collection
      this.collection.ids = column_list.map(obj => obj.id)
      this.dialogVisible = true
      this.column_list = column_list.map(obj => {
        return {
          custom_name: obj.custom_name,
          id: obj.id
        }
      })
      return new Promise(((resolve, reject) => {
        this.resolve = resolve
      }))
    },
    async onSave() {
      let order_text = ""
      if (this.column_list) {
        order_text = JSON.stringify(this.column_list.map(obj => obj.id))
      }
      this.collection.folder_order = order_text
      let re
      if (this.collection.id) {
        re = await web_util.getHttp().post("/update_collection", this.collection)
      } else {
        re = await web_util.getHttp().post("/new_collection", this.collection)
      }
      this.dialogVisible = false
      this.resolve(re.data)
      this.$message.success("saved")
    }
  }
}
</script>
<style scoped>
.the_drag_item {
  cursor: default;
  border: 1px lightgray solid;
  margin: 10px;
}

</style>
