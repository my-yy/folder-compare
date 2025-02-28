<template>
  <el-dialog title="Folder" :visible.sync="dialogVisible" width="70%" :close-on-click-modal="false">
    <div>
      <el-form label-width="100px">
        <el-form-item label="路径">
          <el-input v-model="folder.path" type="textarea" :rows="4"></el-input>
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="folder.name"></el-input>
        </el-form-item>
        <el-form-item label="Desc">
          <el-input v-model="folder.desc" type="textarea" :rows="5"></el-input>
        </el-form-item>
        <!--        <el-form-item label="是否为gt">-->
        <!--          <el-switch v-model="folder.is_gt"></el-switch>-->
        <!--        </el-form-item>-->
      </el-form>

    </div>
    <div style="text-align: center">
      <el-button type="primary" @click="onSave">确 定</el-button>
    </div>

  </el-dialog>
</template>

<script>
import web_util from "@/utils/web_util";


export default {
  name: 'Empty',
  components: {},
  props: [],
  data() {
    return {
      dialogVisible: false,
      folder: {
        path: "",
        name: "",
        desc: "",
        is_gt: false,
      },
      resolve: null,
    }
  },
  mounted() {
    // this.folder.path = "/workspace/audio_team/usr/cgy/1_projects/65_cosyvoice-flow/data/music30"
    // this.folder.name = "music30"
    // this.folder.desc = "music30"
    // this.folder.is_gt = true
  },

  methods: {
    newFolder(content_type = 'wav') {
      this.folder = {
        path: "",
        name: "",
        desc: "",
        is_gt: false,
        content_type: content_type
      }
      this.dialogVisible = true
      return new Promise(((resolve, reject) => {
        this.resolve = resolve
      }))
    },
    editFolder(folder) {
      this.folder = folder
      this.dialogVisible = true
      return new Promise(((resolve, reject) => {
        this.resolve = resolve
      }))
    },
    async onSave() {
      let re
      if (this.folder.id) {
        re = await web_util.getHttp().post("/update_folder", this.folder)
      } else {
        re = await web_util.getHttp().post("/new_folder", this.folder)
      }
      // console.log(data)
      this.$message.success("保存成功")
      this.dialogVisible = false
      this.resolve(re.data)
      this.$emit("save", re.data)
    }

  }
}
</script>
<style scoped>

</style>
