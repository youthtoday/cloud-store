<!--
 * @Description:
 * @Author: hai-27
 * @Date: 2020-02-07 16:23:00
 * @LastEditors: hai-27
 * @LastEditTime: 2020-03-12 19:36:46
 -->
<template>
  <div class="about" id="about" name="about">
    <div class="about-header">
      <div class="about-title">
        <i class="el-icon-tickets" style="color: #ff6700;"></i>
        Administrating Store
      </div>
    </div>
    <div class="about-content" >
      <div>
        <br/>
        <h3>Administrator Identification (YOU MUST ENTER A VALID TOKEN)</h3><br/>
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item>
            <el-input v-model="token" placeholder="token" />
          </el-form-item>
        </el-form>
      </div>
    <div>
      <h3>Manage User</h3>
      <br/>
      <a style="color: darkgrey">Update User Information</a>
      <el-form :inline="true"  class="demo-form-inline">
        <el-form-item>
          <el-input v-model="username" placeholder="username" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="password" placeholder="password" />
        </el-form-item>
         <el-form-item>
          <el-input v-model="email" placeholder="email" />
        </el-form-item>
        <el-button @click="update">update</el-button>
      </el-form>
    </div>
      <div>
        <a style="color: darkgrey">Remove User</a>
        <el-form :inline="true"  class="demo-form-inline">
          <el-form-item>
            <el-input v-model="username2" placeholder="username" />
          </el-form-item>
          <el-button @click="user_remove">remove</el-button>
        </el-form>
      </div>

      <h3>Manage Products</h3>
      <div>
        <br/>
        <a style="color: darkgrey">Set Product Stock</a>
        <el-form :inline="true"  class="demo-form-inline">
          <el-form-item>
            <el-input v-model="product_name" placeholder="product name" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="product_num" placeholder="Set num to" />
          </el-form-item>
          <el-button @click="product_setNum">Set</el-button>
        </el-form>
        <a style="color: darkgrey">Retrieve Categories</a>
        <el-form :inline="true"  class="demo-form-inline">
          <el-button @click="get">Retrieve</el-button>
        </el-form>
      </div>
      <br/>
      <h3>Manage Orders</h3>
      <div>
        <br/>
        <a style="color: darkgrey">Create An Order</a>
        <el-form :inline="true"  class="demo-form-inline">
          <el-form-item>
            <el-input v-model="username3" placeholder="username" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="product_id" placeholder="product id" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="product_num2" placeholder="number" />
          </el-form-item>
          <el-button @click="order_create">create</el-button>
        </el-form>
        <a style="color: darkgrey">Remove An Order</a>
        <el-form :inline="true"  class="demo-form-inline">
        <el-form-item>
          <el-input v-model="order_id" placeholder="order id" />
        </el-form-item>
        <el-form-item>
          <el-button @click="order_remove">remove</el-button>
        </el-form-item>
        </el-form>
      </div>


    </div>
  </div>
</template>

<script>

// import { ref } from 'vue'
// const textarea = ref('')
export default {
  data() {
    return {
      token:'',
      username:'',
      password:'',
      email:'',
      username2:'',
      product_name:'',
      product_num:'',
      username3:'',
      product_id:'',
      product_num2:'',
      order_id:'',
    }
  },
  methods: {
    update() {
      const api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com/admin/user/update";
      const data = {
        "token": this.token,
        "user_name": this.username,
        "password": this.password,
        "email": this.email
      };
      this.$axios
          .post(api, data)
          .then(res => {
            alert(res.data.msg)
          })
    },
    user_remove() {
      const api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com/admin/user/remove";
      const data = {
        "token": this.token,
        "user_name": this.username2
      };
      this.$axios
          .post(api, data)
          .then(res => {alert(res.data.msg)})
    },
    product_setNum() {
      const api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com/admin/product/setNum";
      const data = {
        "token": this.token,
        "product_name": this.product_name,
        "product_num": parseInt(this.product_num)
      };
      this.$axios
          .post(api, data)
          .then(res => {alert(res.data.msg)})
    },
    get() {
      const api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com/admin/product/categories";
      this.$axios
          .get(api)
          .then(res => alert(res.data.msg))
    },
    order_create() {
      const api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com/admin/order/create";
      const data = {
        "username": this.username3,
        "product_id": parseInt(this.product_id),
        "product_num": parseInt(this.product_num2)
      };
      this.$axios
          .post(api, data)
          .then(res => alert(res.data.msg))
    },
    order_remove() {
      const api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com/admin/order/remove";
      const data = {
        "order_id": parseInt(this.order_id)
      };
      this.$axios
          .post(api, data)
          .then(res => alert(res.data.msg))
    }
  }
}
</script>
<style scoped>
.about {
  background-color: #f5f5f5;
}
.about .about-header {
  height: 64px;
  background-color: #fff;
  border-bottom: 2px solid #ff6700;
}
.about .about-header .about-title {
  width: 1225px;
  margin: 0 auto;
  height: 64px;
  line-height: 64px;
  font-size: 28px;
}
.about .content {
  padding: 20px 0;
  width: 1225px;
  margin: 0 auto;
}
.about .content .goods-list {
  margin-left: -13.7px;
  overflow: hidden;
}
.about .about-content {
  width: 1225px;
  margin: 0 auto;
  background-color: #fff;
}
</style>
