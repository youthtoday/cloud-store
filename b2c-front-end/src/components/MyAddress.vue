<template>
  <div id="addressadd">
    <el-dialog title="Save Address" width="400px" center :visible.sync="isAdd">
      <el-form
        :model="address"
        status-icon
        ref="ruleForm"
        class="demo-ruleForm"
      >
        <el-form-item prop="linkman">
          <el-input
            prefix-icon="el-icon-user-solid"
            placeholder="Please enter linkman!"
            v-model="address.linkman"
          ></el-input>
        </el-form-item>
        <el-form-item prop="phone">
          <el-input
            prefix-icon="el-icon-view"
            type="text"
            placeholder="please enter phone number!"
            v-model="address.phone"
          ></el-input>
        </el-form-item>
        <el-form-item prop="address">
          <el-input
            prefix-icon="el-icon-view"
            type="text"
            placeholder="please enter detailed address!"
            v-model="address.address"
          ></el-input>
        </el-form-item>
      
        <el-form-item>
          <el-button size="medium" type="primary" @click="save()" style="width:100%;">save</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: "address",
  props: ["address"],
  data() {         
    return {
      isAdd: false, // 控制注册组件是否显示
      address: {
        linkname: "",
        phone: "",
        address: ""
      }
  },
  watch: {
    // 监听父组件传过来的register变量，设置this.isRegister的值
    isAdd: function(val) {
      if (val) {
        this.isAdd = val;
      }
    }
  },
  methods: {
    save() {
      // 通过element自定义表单校验规则，校验用户输入的用户信息
    
        //如果通过校验开始注册
          this.$axios
            .post("https://keimui43t1.execute-api.us-east-1.amazonaws.com/user/address/save", {
                this.address
            })
            .then(res => {
              // “001”代表注册成功，其他的均为失败
              if (res.data.code === "001") {
                // 隐藏注册组件
                this.isAdd = false;
                // 弹出通知框提示注册成功信息
                this.notifySucceed(res.data.msg);
              } else {
                // 弹出通知框提示注册失败信息
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
<style>
</style>
