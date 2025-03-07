<template>
  <div class="home">
    <div class="topbar">
      <div>
        <el-button size="small" @click="$router.push('/')" icon="el-icon-s-home"></el-button>
        <el-button size="small" @click="onSearch" icon="el-icon-search"></el-button>
        <el-button size="small" @click="onCreateFolderClick" icon="el-icon-plus"></el-button>
      </div>
      <div>
        <div v-if="collection" class="title_bar">
          <div>{{ collection.name }}
            <el-link icon="el-icon-edit-outline" @click="updateCollection"></el-link>
          </div>
          <div class="desc">{{ collection.desc }}</div>
        </div>
      </div>
      <div>
        <el-button size="small" v-if="!collection" @click="newCollection">NewCollection</el-button>
      </div>
    </div>


    <div class="column_wrapper">
      <MyTableView :all_data="folder_list" @close_folder="onCloseFolder" @edit_folder="onEditFolder"/>
    </div>

    <FolderDialog ref="FolderDialog"/>
    <CollectionDialog ref="CollectionDialog" @delete="$router.replace('/')"/>
    <SearchFolderDialog ref="SearchFolderDialog" @select="onAddFolderBySearch" :cur_folders="folder_list"/>
  </div>
</template>

<script>
import web_util from "@/utils/web_util";
import LazyAudio from "@/components/LazyAudio.vue";
import FolderDialog from "@/components/FolderDialog.vue";
import CollectionDialog from "@/components/CollectionDialogV2.vue";
import SearchFolderDialog from "@/components/SearchFolderDialog.vue";
import MyTableView from "@/components/MyTableView.vue";

export default {
  name: 'HomeView',
  components: {
    FolderDialog, LazyAudio, CollectionDialog, SearchFolderDialog, MyTableView
  },
  props: ['id'],
  data() {
    return {
      collection: null,
      folder_list: [],
      all_folders: [],
      options: [],
    }
  },
  async mounted() {

    this.refreshOptionList()


    //1. 获取collection
    const {data} = await web_util.getHttp().post("/get_collection", {'id': parseInt(this.id)})
    this.collection = data

    //2. 获取collection的folder
    const re = await web_util.getHttp().post("/get_folders_of_collection", {'id': parseInt(this.id)})
    for (const f of re.data) {
      try {
        const {data} = await web_util.getHttp().post("/parse_folder", {'id': f.id})
        this.folder_list.push(data)
      } catch (e) {
        console.log(e)
        this.$message.error("解析folder失败：" + f.id)
      }
    }
  },
  computed: {},
  methods: {

    async onSearch() {
      this.$refs.SearchFolderDialog.show()
    },
    async refreshOptionList() {
      const {data} = await web_util.getHttp().post("/get_all_folder")
      this.all_folders = data
      //创建options
      this.options = this.all_folders.map(item => {
        let label = item.name
        if (item.desc) {
          label = label + " " + item.desc
        }

        return {
          value: item.path,
          label: label
        }
      })
    },
    async onCreateFolderClick() {
      const f = await this.$refs.FolderDialog.newFolder()
      await this.addFolderByNewCreateOrBySearch(f)
    },
    async onAddFolderBySearch(f) {
      await this.addFolderByNewCreateOrBySearch(f)
    },
    async addFolderByNewCreateOrBySearch(obj) {
      //2.更新collection的order
      await this.addNewFolderIdInCollection(obj.id)

      //3.更新folder_list
      try {
        const re = await web_util.getHttp().post("/parse_folder", {'id': obj.id})
        this.folder_list.push(re.data)
      } catch (e) {
        console.log(e)
        this.$message.error("解析folder内容失败" + e)
      }

      //4.更新选项：
      this.$refs.SearchFolderDialog.refreshOptionList()
    },
    async addNewFolderIdInCollection(id) {
      const exist_ids = this.getCollectionFolderIds(this.collection)
      console.log("exist_ids", exist_ids)
      exist_ids.push(id)
      await this.updateCollectionFolderIds(exist_ids)
    },
    getCollectionFolderIds(collection) {
      const folder_order_str = collection.folder_order
      let exist_ids = []
      if (folder_order_str) {
        exist_ids = JSON.parse(folder_order_str)
      }
      return exist_ids
    },
    async updateCollectionFolderIds(exist_ids) {
      const folder_order = JSON.stringify(exist_ids)
      await web_util.getHttp().post("/update_collection", {id: this.id, folder_order: folder_order})
      this.collection.folder_order = folder_order
    },
    async onEditFolder(column) {
      const data = await this.$refs.FolderDialog.editFolder(column)
      this.$refs.SearchFolderDialog.refreshOptionList()
    },
    async onCloseFolder(f) {
      //从this.folder_list中删除folder
      this.folder_list = this.folder_list.filter(item => item !== f)
      //更新oder_list
      const exist_ids = this.getCollectionFolderIds(this.collection)
      exist_ids.splice(exist_ids.indexOf(f.id), 1)
      await this.updateCollectionFolderIds(exist_ids)

    },
    async newCollection() {
      const data = await this.$refs.CollectionDialog.newCollection(this.folder_list)
      console.log("data", data)
      this.$router.replace("/collection/" + data.id)
      this.collection = data
    },
    async updateCollection() {
      this.$refs.CollectionDialog.updateCollection(this.collection, this.folder_list)
    }
  }
}
</script>
<style scoped>

.topbar {
  display: flex;
  margin-bottom: 10px;
}

.topbar > div {
  flex: 1;
}

.title_bar {
  text-align: center;
}

.title_bar > .desc {
  font-size: small;
  color: gray;
  white-space: pre-wrap;
}

.folder_input input {
  width: 80vw;
}

.input_wrapper {
  display: flex;
  flex-direction: row;
  margin-bottom: 10px;
}

.column_wrapper {
  display: flex;
  flex-direction: row;
}


.item {
  margin-bottom: 20px;
  height: 100px;
}

.item_name {
  font-size: xx-small;
  width: 100%; /* 或者你可以设置一个固定宽度 */
  /*white-space: nowrap; !* 确保文本在一行内显示 *!*/
  /*overflow: hidden; !* 隐藏超出部分 *!*/
  /*text-overflow: ellipsis; !* 当文本被截断时显示省略号 *!*/
  color: gray;
}

.one_column {
  width: 300px;
  margin-right: 10px;
}

.column_desc {
  height: 50px;
  margin-bottom: 10px;
}

.item_list2 {
  border: 1px black solid;
  overflow-y: auto;
  max-height: calc(100vh - 200px);
}


.column_name {
  font-size: xx-small;
  font-weight: bold;
  width: 100%; /* 或者你可以设置一个固定宽度 */
  white-space: nowrap; /* 确保文本在一行内显示 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 当文本被截断时显示省略号 */
}

.single_wav_score {
  font-size: small;
}

</style>
