<template>
  <div v-if="collection">
    <div class="topbar">
      <div>
        <el-button size="small" @click="$router.push('/')" icon="el-icon-s-home"></el-button>
        <el-button size="small" @click="onSearch" icon="el-icon-search"></el-button>
        <el-button size="small" @click="createFolder" icon="el-icon-plus"></el-button>
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
      </div>
    </div>


    <div>
      <div v-for="f in folder_list">
        <i class="el-icon-close" @click="onRemoveFolder(f)"></i>
        <span> {{ f.custom_name || f.name }}</span>
        <el-link icon="el-icon-edit" @click="onEditFolder(f)"></el-link>
      </div>
    </div>
    <div class="display_wrapper">
      <div ref="chart" style="width: 70vw; height: 60vh;margin: 0 auto"></div>
      <!--      <div class="raw_step_eval_logs">-->
      <!--        <div v-for="obj in obj_list" :key="obj.name">-->
      <!--          {{ obj }}-->
      <!--        </div>-->
      <!--      </div>-->
    </div>
    <FolderDialog ref="FolderDialog"/>
    <CollectionDialog ref="CollectionDialog" @delete="onCollectionDeleted"/>
    <SearchFolderDialog ref="SearchFolderDialog" @select="onAddFolder"/>
  </div>
</template>

<script>
import web_util from "@/utils/web_util";
import * as echarts from 'echarts';
import FolderDialog from "@/components/FolderDialog.vue";
import CollectionDialog from "@/components/CollectionDialogV2.vue";
import SearchFolderDialog from "@/components/SearchFolderDialog.vue";

export default {
  name: 'Empty',
  components: {SearchFolderDialog, CollectionDialog, FolderDialog},
  props: ["id"],
  data() {
    return {
      collection: null,
      folder_list: [],
    }
  },
  async mounted() {
    //1. 获取collection
    const {data} = await web_util.getHttp().post("/get_collection", {'id': parseInt(this.id)})
    this.collection = data

    //2. 获取collection的folder
    const re = await web_util.getHttp().post("/get_folders_of_collection", {'id': parseInt(this.id)})
    this.folder_list = re.data
    const folder_list = re.data
    console.log(this.folder_list)

    //等待页面渲染完成
    await this.$nextTick()

    //3. 绘图
    this.chart = echarts.init(this.$refs.chart);
    this.setChartOption()

  },
  methods: {
    async onSearch() {
      this.$refs.SearchFolderDialog.show()
    },
    async createFolder() {
      const obj = await this.$refs.FolderDialog.newFolder('ckpt')
      const id = obj.id

      //保存到当前collection中
      await this.addNewFolderIdInCollection(id)

      //3.push进去
      this.folder_list.push(obj)
    },
    async addNewFolderIdInCollection(id) {
      const exist_ids = this.getCollectionFolderIds(this.collection)
      exist_ids.push(id)
      await this.updateCollectionFolderIds(exist_ids)
    },

    async updateCollectionFolderIds(exist_ids) {
      const folder_order = JSON.stringify(exist_ids)
      const {data} = await web_util.getHttp().post("/update_collection", {id: this.id, folder_order: folder_order})
      this.collection.folder_order = folder_order
    },
    getCollectionFolderIds(collection) {
      const folder_order_str = collection.folder_order
      let exist_ids = []
      if (folder_order_str) {
        exist_ids = JSON.parse(folder_order_str)
      }
      return exist_ids
    },
    async setChartOption() {
      const series = []
      const legendData = []; // 用于存储图例数据
      const legend_selected = {}
      for (const fobj of this.folder_list) {
        let data
        try {
          const re = await web_util.getHttp().post("/parse_ckpt_folder", {path: fobj.path})
          data = re.data
        } catch (e) {
          console.log(e)
          this.$message.error("加载失败")
          continue
        }
        const obj_list = data.list

        const seriesItem = {
          name: fobj.custom_name || fobj.name,
          type: 'line',
          data: obj_list.map(item => [item.step, item.seed50_recons_sim]),
          // visible: false,
        };
        series.push(seriesItem);
        legendData.push(seriesItem.name); // 将曲线名称添加到图例数据中
        legend_selected[seriesItem.name] = true
      }

      const option = {
        // title: {
        //   text: '曲线图'
        // },
        legend: {
          data: legendData, // 使用图例数据
          selected: legend_selected //用于显示，隐藏
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'value',
          name: 'Step',
        },
        yAxis: {
          type: 'value',
          name: 'seed50_recons_sim'
        },
        series: series,
        // dataZoom: [
        //   {
        //     type: 'slider', // 滑动条型
        //     start: 0, // 初始显示范围的起始百分比
        //     end: 100 // 初始显示范围的结束百分比
        //   },
        // ],
        dataZoom2: [
          {
            id: 'dataZoomX',
            type: 'slider', // 内置型缩放
            xAxisIndex: [0], // 控制 X 轴
            filterMode: 'filter', // X 轴缩放模式
            start: 0, // 初始显示范围的起始百分比
            end: 100 // 初始显示范围的结束百分比
          },
          {
            id: 'dataZoomY',
            type: 'slider', // 内置型缩放
            yAxisIndex: [0], // 控制 Y 轴
            filterMode: 'empty', // Y 轴缩放模式
            start: 0,
            end: 100
          }
        ]
      };
      this.chart.setOption(option);
    },


    async onRemoveFolder(f) {
      const exist_ids = this.getCollectionFolderIds(this.collection)
      exist_ids.splice(exist_ids.indexOf(f.id), 1)
      await this.updateCollectionFolderIds(exist_ids)
      this.folder_list.splice(this.folder_list.indexOf(f), 1)
    },
    async updateCollection() {
      this.$refs.CollectionDialog.updateCollection(this.collection, this.folder_list)
    },
    async onEditFolder(f) {
      const data = await this.$refs.FolderDialog.editFolder(f)
      // this.$refs.SearchFolderDialog.refreshOptionList()
    },
    async onAddFolder(f) {
      this.folder_list.push(f)
      this.setChartOption()
      await this.addNewFolderIdInCollection(f.id)
    },
    onCollectionDeleted() {
      this.$router.replace("/")
    }
  }
}
</script>
<style scoped>
.display_wrapper {
  display: flex;
  flex-direction: row;
}

.raw_step_eval_logs {
  font-size: small;
}

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

</style>
