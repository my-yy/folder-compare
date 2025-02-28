<template>
  <el-dialog title="Collection" :visible.sync="dialogVisible" width="70%">
    <div>
      <el-form label-width="100px">
        <el-form-item label="Orders" v-if="folder_list.length>0">
          <div>
            <draggable v-model="folder_list" group="people">
              <span class="the_drag_item" v-for="element in folder_list" :key="element.id">{{
                  element.name
                }}</span>
            </draggable>

          </div>
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="collection.name"></el-input>
        </el-form-item>
        <el-form-item label="Desc">
          <el-input v-model="collection.desc" type="textarea" :rows="5"></el-input>
        </el-form-item>
        <el-form-item label="Raw" v-if="collection.raw_folders">
          <el-input v-model="collection.raw_folders" type="textarea" :rows="5"></el-input>
        </el-form-item>
        <el-form-item label="Delete">
          <el-link @click="onDeleteCollection">删除</el-link>
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
      folder_list: []
    }
  },
  mounted() {

  },
  methods: {
    onEnd() {
      console.log('拖拽结束');
    },
    updateCollection(collection, folder_list) {
      this.collection = collection
      this.collection.ids = folder_list.map(obj => obj.id)
      this.dialogVisible = true
      this.folder_list = folder_list.map(obj => {
        return {
          name: obj.name,
          id: obj.id
        }
      })
      return new Promise(((resolve, reject) => {
        this.resolve = resolve
      }))
    },
    async onSave() {
      let order_text = ""
      if (this.folder_list) {
        order_text = JSON.stringify(this.folder_list.map(obj => obj.id))
      }
      this.collection.folder_order = order_text
      let re
      re = await web_util.getHttp().post("/update_collection", this.collection)
      this.dialogVisible = false
      this.resolve(re.data)
      this.$message.success("saved")
    },
    async onDeleteCollection() {
      try {
        await this.$confirm('此操作将永久删除该记录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
      } catch (e) {
        return
      }
      console.log("1")
      await web_util.getHttp().post("/delete_collection", this.collection)
      console.log("已经删除")

      this.$message.success("删除成功")
      this.$emit("delete")
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
