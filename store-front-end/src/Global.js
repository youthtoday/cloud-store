exports.install = function (Vue) {
  Vue.prototype.$target = "https://keimui43t1.execute-api.us-east-1.amazonaws.com"; // 线上后端地址
  Vue.prototype.$api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com"
  //  Vue.prototype.$target = "http://127.0.0.1:5000/"; // 本地后端地址
  // 封装提示成功的弹出框
  Vue.prototype.notifySucceed = function (msg) {
    this.$notify({
      title: "Success",
      message: msg,
      type: "success",
      offset: 100
    });
  };
  // 封装提示失败的弹出框
  Vue.prototype.notifyError = function (msg) {
    this.$notify.error({
      title: "Fail",
      message: msg,
      offset: 100
    });
  };
}
