<template>
  <div id="myLogin">
    <el-dialog title="login" width="300px" center :visible.sync="isLogin">
      <el-form :model="LoginUser" :rules="rules" status-icon ref="ruleForm" class="demo-ruleForm">
        <el-form-item prop="name">
          <el-input
              prefix-icon="el-icon-user-solid"
              placeholder="please enter your username"
              v-model="LoginUser.name"></el-input>
        </el-form-item>
        <el-form-item prop="pass">
          <el-input
            prefix-icon="el-icon-view"
            type="password"
            placeholder="please enter your password"
            v-model="LoginUser.pass"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" type="primary" @click="Login" style="width:100%;">login</el-button>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" type="primary" @click="LoginOauth" style="width:100%;">associate with Github</el-button>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" type="primary" @click="LoginOauth2" style="width:100%;">login via Github</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
import { mapActions } from "vuex";
// import router from "@/router";

export default {
  name: "MyLogin",
  data() {
    // 用户名的校验方法
    let validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("please enter username"));
      }
      // 用户名以字母开头,长度在5-16之间,允许字母数字下划线
      const userNameRule = /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/;
      if (userNameRule.test(value)) {
        this.$refs.ruleForm.validateField("checkPass");
        return callback();
      } else {
        return callback(new Error("Must start with a letter and length of 5 to 16. Underscores are allowed."));
      }
    };
    // 密码的校验方法
    let validatePass = (rule, value, callback) => {
      if (value === "") {
        return callback(new Error("please enter password"));
      }
      // 密码以字母开头,长度在6-18之间,允许字母数字和下划线
      const passwordRule = /^[a-zA-Z]\w{5,17}$/;
      if (passwordRule.test(value)) {
        this.$refs.ruleForm.validateField("checkPass");
        return callback();
      } else {
        return callback(
          new Error("Must start with a letter and length of 6 to 18. Underscores are allowed.")
        );
      }
    };
    return {
      LoginUser: {
        name: "",
        pass: ""
      },
      // 用户信息校验规则,validator(校验方法),trigger(触发方式),blur为在组件 Input 失去焦点时触发
      rules: {
        name: [{ validator: validateName, trigger: "blur" }],
        pass: [{ validator: validatePass, trigger: "blur" }]
      }
    };
  },
  computed: {
    // 获取vuex中的showLogin，控制登录组件是否显示
    isLogin: {
      get() {
        return this.$store.getters.getShowLogin;
      },
      set(val) {
        this.$refs["ruleForm"].resetFields();
        this.setShowLogin(val);
      }
    }
  },
  methods: {
    ...mapActions(["setUser", "setShowLogin"]),
    Login() {
      // 通过element自定义表单校验规则，校验用户输入的用户信息
      this.$refs["ruleForm"].validate(valid => {
        //如果通过校验开始登录
        if (valid) {
          this.$axios
            .post("https://keimui43t1.execute-api.us-east-1.amazonaws.com/user/login", {
              userName: this.LoginUser.name,
              password: this.LoginUser.pass
            })
            .then(res => {
              // “001”代表登录成功，其他的均为失败
              if (res.data.code === "001") {
                // 隐藏登录组件
                this.isLogin = false;
                // 登录信息存到本地
                let user = JSON.stringify(res.data.data);
                localStorage.setItem("user", user);
                // 登录信息存到vuex
                this.setUser(res.data.data);
                // 弹出通知框提示登录成功信息
                this.notifySucceed(res.data.msg);
              } else {
                // 清空输入框的校验状态
                this.$refs["ruleForm"].resetFields();
                // 弹出通知框提示登录失败信息
                this.notifyError(res.data.msg);
              }
            })
            // .catch(err => {
            //   return Promise.reject(err);
            // });
        }
        // else {
        //   return false;
        // }
      });
    },
    LoginOauth() {
      this.$axios
          .get("https://keimui43t1.execute-api.us-east-1.amazonaws.com/user/oauth",{})
          .then(res => {
            if (res.data.code === "001") {
              // 跳转到新页面
              window.open(res.data.url, "blank")
            } else {
              // 清空输入框的校验状态
              this.$refs["ruleForm"].resetFields();
              // 弹出通知框提示登录失败信息
              this.notifyError(res.data.msg);
            }
          })
    },
    ...mapActions(["setUser", "setShowLogin"]),
    LoginOauth2() {
      // 通过element自定义表单校验规则，校验用户输入的用户信息
      this.$axios
          .get("https://keimui43t1.execute-api.us-east-1.amazonaws.com/oauth/data",{})
          .then(res => {
            if (res.data.code === "001") {
              // 隐藏登录组件
              this.isLogin = false;
              // 登录信息存到本地
              let user = JSON.stringify(res.data.data);
              localStorage.setItem("user", user);
              // 登录信息存到vuex
              this.setUser(res.data.data);
              // 弹出通知框提示登录成功信息
              this.notifySucceed(res.data.msg);
            } else {
              // 清空输入框的校验状态
              this.$refs["ruleForm"].resetFields();
              // 弹出通知框提示登录失败信息
              this.notifyError(res.data.msg);
            }
          })
    }
  }
};
</script>
<style>
</style>
