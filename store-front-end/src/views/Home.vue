<template>
  <div class="home" id="home" name="home">
    <!-- 轮播图 -->
<!--    <div class="block">-->
<!--      <el-carousel height="460px">-->
<!--        <el-carousel-item v-for="item in carousel" :key="item.carousel_id">-->
<!--         <router-link :to="{ path: '/goods/details', query: {productID:item.product_id} }">-->
<!--          <img style="height:460px;" :src="item.imgPath.includes('http:')?item.imgPath:$target + item.imgPath" :alt="item.describes" />-->
<!--            </router-link>-->
<!--        </el-carousel-item>-->

<!--      </el-carousel>-->
<!--    </div>-->
    <!-- 轮播图END -->
    <div class="main-box">
      <div class="main">
        <!-- 手机商品展示区域 -->
        <div class="phone">
          <div class="box-hd">
            <div class="title">Phone</div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <router-link to>
                <img :src="'https://6156-pictures.s3.amazonaws.com/' +'public/imgs/phone/phone.png'" />
              </router-link>
            </div>
            <div class="list">
              <MyList :list="phoneList" :isMore="true"></MyList>
            </div>
          </div>
        </div>
        <!-- 手机商品展示区域END -->

        <!-- 家电商品展示区域 -->
        <div class="appliance" id="promo-menu">
          <div class="box-hd">
            <div class="title">Electrics</div>
            <div class="more" id="more">
              <MyMenu :val="2" @fromChild="getChildMsg">
                <span slot="1">Hot</span>
                <span slot="2">TV</span>
              </MyMenu>
            </div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <ul>
                <li>
                  <img :src="'https://6156-pictures.s3.amazonaws.com/' +'public/imgs/appliance/appliance-promo1.png'" />
                </li>
                <li>
                  <img :src="'https://6156-pictures.s3.amazonaws.com/' +'public/imgs/appliance/appliance-promo2.png'" />
                </li>
              </ul>
            </div>
            <div class="list">
              <MyList :list="applianceList" :isMore="true"></MyList>
            </div>
          </div>
        </div>
        <!-- 家电商品展示区域END -->

        <!-- 配件商品展示区域 -->
        <div class="accessory" id="promo-menu">
          <div class="box-hd">
            <div class="title">Supplies</div>
            <div class="more" id="more">
              <MyMenu :val="3" @fromChild="getChildMsg2">
                <span slot="1">Hot</span>
                <span slot="2">Protective Shell</span>
                <span slot="3">Charger</span>
              </MyMenu>
            </div>
          </div>
          <div class="box-bd">
            <div class="promo-list">
              <ul>
                <li>
                  <img :src="'https://6156-pictures.s3.amazonaws.com/' +'public/imgs/accessory/accessory-promo1.png'" alt />
                </li>
                <li>
                  <img :src="'https://6156-pictures.s3.amazonaws.com/' +'public/imgs/accessory/accessory-promo2.png'" alt />
                </li>
              </ul>
            </div>
            <div class="list">
              <MyList :list="accessoryList" :isMore="true"></MyList>
            </div>
          </div>
        </div>
        <!-- 配件商品展示区域END -->
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      carousel: "", // 轮播图数据
      phoneList: "", // 手机商品列表
      miTvList: "", // 小米电视商品列表
      applianceList: "", // 家电商品列表
      applianceHotList: "", //热门家电商品列表
      accessoryList: "", //配件商品列表
      accessoryHotList: "", //热门配件商品列表
      protectingShellList: "", // 保护套商品列表
      chargerList: "", //充电器商品列表
      applianceActive: 1, // 家电当前选中的商品分类
      accessoryActive: 1 // 配件当前选中的商品分类
    };
  },
  watch: {
    // 家电当前选中的商品分类，响应不同的商品数据
    applianceActive: function(val) {
      // 页面初始化的时候把applianceHotList(热门家电商品列表)直接赋值给applianceList(家电商品列表)
      // 所以在切换商品列表时判断applianceHotList是否为空,为空则是第一次切换,把applianceList赋值给applianceHotList
      if (this.applianceHotList == "") {
        this.applianceHotList = this.applianceList;
      }
      if (val == 1) {
        // 1为热门商品
        this.applianceList = this.applianceHotList;
        return;
      }
      if (val == 2) {
        // 2为电视商品
        this.applianceList = this.miTvList;
        return;
      }
    },
    accessoryActive: function(val) {
      // 页面初始化的时候把accessoryHotList(热门配件商品列表)直接赋值给accessoryList(配件商品列表)
      // 所以在切换商品列表时判断accessoryHotList是否为空,为空则是第一次切换,把accessoryList赋值给accessoryHotList
      if (this.accessoryHotList == "") {
        this.accessoryHotList = this.accessoryList;
      }
      if (val == 1) {
        // 1为热门商品
        this.accessoryList = this.accessoryHotList;
        return;
      }
      if (val == 2) {
        // 2为保护套商品
        this.accessoryList = this.protectingShellList;
        return;
      }
      if (val == 3) {
        //3 为充电器商品
        this.accessoryList = this.chargerList;
        return;
      }
    }
  },
  created() {
    // 获取轮播图数据
    this.$axios
      .post("https://keimui43t1.execute-api.us-east-1.amazonaws.com/carousel/list", {})
      .then(res => {
        this.carousel = res.data.data;
      })
      .catch(err => {
        return Promise.reject(err);
      });
    // 获取各类商品数据
    this.getPromo("Phone", "phoneList");
    this.getPromo("TV", "miTvList");
    this.getPromo("Protective Shell", "protectingShellList");
    this.getPromo("Charger", "chargerList");
    this.getPromo(
      ["TV", "AC", "Washing Machine"],
      "applianceList",
      "https://keimui43t1.execute-api.us-east-1.amazonaws.com/product/hots"
    );
    this.getPromo(
      ["Protective Shell", "Protective Film", "Charger", "Power Bank"],
      "accessoryList",
      "https://keimui43t1.execute-api.us-east-1.amazonaws.com/product/hots"
    );
  },
  methods: {
    // 获取家电模块子组件传过来的数据
    getChildMsg(val) {
      this.applianceActive = val;
    },
    // 获取配件模块子组件传过来的数据
    getChildMsg2(val) {
      this.accessoryActive = val;
    },
    // 获取各类商品数据方法封装
    getPromo(categoryName, val, api) {
      api = api != undefined ? api : "https://keimui43t1.execute-api.us-east-1.amazonaws.com/product/promo";
      this.$axios
        .post(api, {
          categoryName
        })
        .then(res => {
          this[val] = res.data.data;
        })
        .catch(err => {
          return Promise.reject(err);
        });
    }
  }
};
</script>
<style scoped>
@import "../assets/css/index.css";
</style>
