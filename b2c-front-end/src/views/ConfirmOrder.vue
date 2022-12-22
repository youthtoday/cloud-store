<template>
  <div class="confirmOrder">
    <!-- 头部 -->
    <div class="confirmOrder-header">
      <div class="header-content">
        <p>
          <i class="el-icon-s-order"></i>
        </p>
        <p>Confirm Order</p>
        <router-link to></router-link>
      </div>
    </div>
    <!-- 头部END -->

    <!-- 主要内容容器 -->
    <div class="content">
      <!-- 选择地址 -->
      <div class="section-address">
        <p class="title">shipping address</p>
        <font color='red' size=2>hint: double clicks can clear address</font>
        <br>
        <br>
        <div class="address-body">
          <ul>
        
            <li
              v-for="(item,index) in address"
              :class="confirmAddress==item.id?'in-section':''"
              :key="item.id"
              @click="confirmAddress=item.id"
              @dblclick="removeItem(index)"
            >
              <h2>{{item.linkman}}</h2>
              <p class="phone">{{item.phone}}</p>
              <p class="address"><font color='green'>{{item.address}}</font></p>

           
            </li>
            
            <li class="add-address"  @click="isAdd=true">
              <i class="el-icon-circle-plus-outline"></i>
              <p >save new address</p>
            </li>
          </ul>
        </div>
      </div>
      <!-- 选择地址END -->

      <!-- 商品及优惠券 -->
      <div class="section-goods">
        <p class="title">goods and coupons</p>
        <div class="goods-list">
          <ul>
            <li v-for="item in getCheckGoods" :key="item.id">
              <img :src="item.productImg.includes('http:')?item.productImg:'https://6156-pictures.s3.amazonaws.com/' + item.productImg" />
              <span class="pro-name">{{item.productName}}</span>
              <span class="pro-price">${{item.price}} x {{item.num}}</span>
              <span class="pro-status"></span>
              <span class="pro-total">${{item.price * item.num}}</span>
            </li>
          </ul>
        </div>
      </div>
      <!-- 商品及优惠券END -->

      <!-- 配送方式 -->
      <div class="section-shipment">
        <p class="title">shipment</p>
        <p class="shipment">free shipment</p>
      </div>
      <!-- 配送方式END -->

      <!-- 发票 -->
      <div class="section-invoice">
        <p class="title">receipts</p>
        <p class="invoice">electronic receipts</p>
        <p class="invoice">personal</p>
        <p class="invoice">item details</p>
      </div>
      <!-- 发票END -->

      <!-- 结算列表 -->
      <div class="section-count">
        <div class="money-box">
          <ul>
            <li>
              <span class="title">item counts:</span>
              <span class="value">{{getCheckNum}}</span>
            </li>
            <li>
              <span class="title">overall price:</span>
              <span class="value">${{getTotalPrice}}</span>
            </li>
            <li>
              <span class="title">special offer:</span>
              <span class="value">-$0</span>
            </li>
            <li>
              <span class="title">coupons discount:</span>
              <span class="value">-$0</span>
            </li>
            <li>
              <span class="title">shipment fee</span>
              <span class="value">$0</span>
            </li>
            <li class="total">
              <span class="title">total amount</span>
              <span class="value">
                $<span class="total-price">{{getTotalPrice}}</span>
              </span>
            </li>
          </ul>
        </div>
      </div>
      <!-- 结算列表END -->

      <!-- 结算导航 -->
      <div class="section-bar">
        <div class="btn">
          <router-link to="/shoppingCart" class="btn-base btn-return">back to cart</router-link>
          <a href="javascript:void(0);" @click="addOrder" class="btn-base btn-primary">pay</a>
        </div>
      </div>
      <!-- 结算导航END -->
    </div>
    <!-- 主要内容容器END -->


    <!-- 删除 popover框-->

    <el-dialog
      title="delete hint!"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <span> <font color='red'>{{dialogValue}}</font></span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">cancel</el-button>
        <el-button type="primary" @click="remove()">yes</el-button>
      </span>
    </el-dialog>


    <!-- 弹出框 -->

    <el-dialog title="save address" width="400px" center :visible.sync="isAdd">
      <el-form
        :model="add"
        status-icon
        ref="ruleForm"
        class="demo-ruleForm"
      >
        <el-form-item prop="linkman">
          <el-input
            prefix-icon="el-icon-user-solid"
            placeholder="please enter name"
            v-model="add.linkman"
            maxlength="20"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item prop="phone">
          <el-input
            prefix-icon="el-icon-view"
            type="text"
            placeholder="please enter phone number"
            v-model="add.phone"
            maxlength="11"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item prop="address">
         <el-input
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4}"
            placeholder="please enter detailed address"
            v-model="add.address">
          </el-input>
        </el-form-item>


      
        <el-form-item>
          <el-button size="medium" type="primary" @click="save()" style="width:100%;">save</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>

</template>
<script>
import { mapGetters } from "vuex";
import { mapActions } from "vuex";
export default {
  name: "",
  data() {
    return {
      // 虚拟数据
      confirmAddress: 0, // 选择的地址id,
      isAdd:false,
      dialogVisible:false,  //dialog框显示
      dialogValue: null, //删除提示语
      delId:0,  //删除的id
      delIndex:0,
      //添加地址接口
      add:{
        linkman:"",
        phone:"",
        address:""
      },

      // 地址列表
      address: [
        
      ]
    };
  },
  created() {
    // 如果没有勾选购物车商品直接进入确认订单页面,提示信息并返回购物车
    if (this.getCheckNum < 1) {
      this.notifyError("please proceed after selecting items");
      this.$router.push({ path: "/shoppingCart" });
    }

     // 获取轮播图数据
     this.$axios
      .post("api/user/address/list", {
          user_id: this.$store.getters.getUser.user_id
      })
      .then(res => {
        this.address = res.data.data;
      })
      .catch(err => {
        return Promise.reject(err);
      })
  },
  computed: {
    // 结算的商品数量; 结算商品总计; 结算商品信息
    ...mapGetters(["getCheckNum", "getTotalPrice", "getCheckGoods"])
  },
  methods: {
    ...mapActions(["deleteShoppingCart"]),


    removeItem(index){
      this.dialogValue =  "Are you sure to delete the address of "+this.address[index].linkman+"?";
      this.delId = this.address[index].id;
      this.delIndex  = index; //要删除的下角标
      this.dialogVisible=true
    },

    //删除地址数据!
    remove(){
      this.$axios
        .post("https://keimui43t1.execute-api.us-east-1.amazonaws.com/user/address/remove", {
          id: this.delId
        })
        .then(res => {
          switch (res.data.code) {
            // “001”代表结算成功
            case "001":
               this.delId = 0;
               this.dialogVisible=false
               this.address.splice(this.delIndex,1);
               this.delIndex  = 0; //要删除的下角标
              // 提示结算结果 
              this.notifySucceed(res.data.msg);  
              break;
            default:
              // 提示失败信息
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    },

    save(){

      this.$axios
        .post("https://keimui43t1.execute-api.us-east-1.amazonaws.com/user/address/save", {
          user_id: this.$store.getters.getUser.user_id,
          "add.address": this.add.address,
          "add.linkman": this.add.linkman,
          "add.phone": this.add.phone
        })
        .then(res => {
          switch (res.data.code) {
            // “001”代表结算成功
            case "001":
              this.isAdd = false; //隐藏弹出框
              this.address = res.data.data; //接收新地址内容
              // 提示结算结果 
              this.notifySucceed(res.data.msg);  
              break;
            default:
              // 提示失败信息
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });

    },
    addOrder() {
      this.$axios
        .post("https://keimui43t1.execute-api.us-east-1.amazonaws.com/order/save", {
          user_id: this.$store.getters.getUser.user_id,
          products: this.getCheckGoods
        })
        .then(res => {
          let products = this.getCheckGoods;
          switch (res.data.code) {
            // “001”代表结算成功
            case "001":
              for (let i = 0; i < products.length; i++) {
                const temp = products[i];
                // 删除已经结算的购物车商品
                this.deleteShoppingCart(temp.id);
              }
              // 提示结算结果
              this.notifySucceed(res.data.msg);
              // 跳转我的订单页面
              this.$router.push({ path: "/order" });
              break;
            default:
              // 提示失败信息
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    }
  }
};
</script>
<style scoped>
.confirmOrder {
  background-color: #f5f5f5;
  padding-bottom: 20px;
}
/* 头部CSS */
.confirmOrder .confirmOrder-header {
  background-color: #fff;
  border-bottom: 2px solid #ff6700;
  margin-bottom: 20px;
}
.confirmOrder .confirmOrder-header .header-content {
  width: 1225px;
  margin: 0 auto;
  height: 80px;
}
.confirmOrder .confirmOrder-header .header-content p {
  float: left;
  font-size: 28px;
  line-height: 80px;
  color: #424242;
  margin-right: 20px;
}
.confirmOrder .confirmOrder-header .header-content p i {
  font-size: 45px;
  color: #ff6700;
  line-height: 80px;
}
/* 头部CSS END */

/* 主要内容容器CSS */
.confirmOrder .content {
  width: 1225px;
  margin: 0 auto;
  padding: 48px 0 0;
  background-color: #fff;
}

/* 选择地址CSS */
.confirmOrder .content .section-address {
  margin: 0 48px;
  overflow: hidden;
}
.confirmOrder .content .section-address .title {
  color: #333;
  font-size: 18px;
  line-height: 20px;
  margin-bottom: 20px;
}
.confirmOrder .content .address-body li {
  float: left;
  color: #333;
  width: 220px;
  height: 178px;
  border: 1px solid #e0e0e0;
  padding: 15px 24px 0;
  margin-right: 17px;
  margin-bottom: 24px;
}
.confirmOrder .content .address-body .in-section {
  border: 1px solid #ff6700;
}
.confirmOrder .content .address-body li h2 {
  font-size: 18px;
  font-weight: normal;
  line-height: 30px;
  margin-bottom: 10px;
}
.confirmOrder .content .address-body li p {
  font-size: 14px;
  color: #757575;
}
.confirmOrder .content .address-body li .address {
  padding: 10px 0;
  max-width: 180px;
  max-height: 88px;
  line-height: 22px;
  overflow: hidden;
}
.confirmOrder .content .address-body .add-address {
  text-align: center;
  line-height: 30px;
}
.confirmOrder .content .address-body .add-address i {
  font-size: 30px;
  padding-top: 50px;
  text-align: center;
}
/* 选择地址CSS END */

/* 商品及优惠券CSS */
.confirmOrder .content .section-goods {
  margin: 0 48px;
}
.confirmOrder .content .section-goods p.title {
  color: #333;
  font-size: 18px;
  line-height: 40px;
}
.confirmOrder .content .section-goods .goods-list {
  padding: 5px 0;
  border-top: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
}
.confirmOrder .content .section-goods .goods-list li {
  padding: 10px 0;
  color: #424242;
  overflow: hidden;
}
.confirmOrder .content .section-goods .goods-list li img {
  float: left;
  width: 30px;
  height: 30px;
  margin-right: 10px;
}
.confirmOrder .content .section-goods .goods-list li .pro-name {
  float: left;
  width: 650px;
  line-height: 30px;
}
.confirmOrder .content .section-goods .goods-list li .pro-price {
  float: left;
  width: 150px;
  text-align: center;
  line-height: 30px;
}
.confirmOrder .content .section-goods .goods-list li .pro-status {
  float: left;
  width: 99px;
  height: 30px;
  text-align: center;
  line-height: 30px;
}
.confirmOrder .content .section-goods .goods-list li .pro-total {
  float: left;
  width: 190px;
  text-align: center;
  color: #ff6700;
  line-height: 30px;
}
/* 商品及优惠券CSS END */

/* 配送方式CSS */
.confirmOrder .content .section-shipment {
  margin: 0 48px;
  padding: 25px 0;
  border-bottom: 1px solid #e0e0e0;
  overflow: hidden;
}
.confirmOrder .content .section-shipment .title {
  float: left;
  width: 150px;
  color: #333;
  font-size: 18px;
  line-height: 38px;
}
.confirmOrder .content .section-shipment .shipment {
  float: left;
  line-height: 38px;
  font-size: 14px;
  color: #ff6700;
}
/* 配送方式CSS END */

/* 发票CSS */
.confirmOrder .content .section-invoice {
  margin: 0 48px;
  padding: 25px 0;
  border-bottom: 1px solid #e0e0e0;
  overflow: hidden;
}
.confirmOrder .content .section-invoice .title {
  float: left;
  width: 150px;
  color: #333;
  font-size: 18px;
  line-height: 38px;
}
.confirmOrder .content .section-invoice .invoice {
  float: left;
  line-height: 38px;
  font-size: 14px;
  margin-right: 20px;
  color: #ff6700;
}
/* 发票CSS END */

/* 结算列表CSS */
.confirmOrder .content .section-count {
  margin: 0 48px;
  padding: 20px 0;
  overflow: hidden;
}
.confirmOrder .content .section-count .money-box {
  float: right;
  text-align: right;
}
.confirmOrder .content .section-count .money-box .title {
  float: left;
  width: 126px;
  height: 30px;
  display: block;
  line-height: 30px;
  color: #757575;
}
.confirmOrder .content .section-count .money-box .value {
  float: left;
  min-width: 105px;
  height: 30px;
  display: block;
  line-height: 30px;
  color: #ff6700;
}
.confirmOrder .content .section-count .money-box .total .title {
  padding-top: 15px;
}
.confirmOrder .content .section-count .money-box .total .value {
  padding-top: 10px;
}
.confirmOrder .content .section-count .money-box .total-price {
  font-size: 30px;
}
/* 结算列表CSS END */

/* 结算导航CSS */
.confirmOrder .content .section-bar {
  padding: 20px 48px;
  border-top: 2px solid #f5f5f5;
  overflow: hidden;
}
.confirmOrder .content .section-bar .btn {
  float: right;
}
.confirmOrder .content .section-bar .btn .btn-base {
  float: left;
  margin-left: 30px;
  width: 158px;
  height: 38px;
  border: 1px solid #b0b0b0;
  font-size: 14px;
  line-height: 38px;
  text-align: center;
}
.confirmOrder .content .section-bar .btn .btn-return {
  color: rgba(0, 0, 0, 0.27);
  border-color: rgba(0, 0, 0, 0.27);
}
.confirmOrder .content .section-bar .btn .btn-primary {
  background: #ff6700;
  border-color: #ff6700;
  color: #fff;
}
/* 结算导航CSS */

/* 主要内容容器CSS END */
</style>
