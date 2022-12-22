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
        About Us
      </div>
    </div>
    <div class="about-content" >
      <br/><h2>Feedback</h2><br/><br/>
        <el-input
            style="width: 70%"
            v-model="textarea"
            :rows="10"
            type="textarea"
            placeholder="Please input"
        />
      <br/><br/>
      <el-button @click="send">send</el-button>


      <!--      <MyMarkdown></MyMarkdown>-->
      <br/><br/><br/><br/><br/><br/>
      This is a group project of COMS E6156 Topics in Software Development: Cloud Computing at Columbia University.

    </div>
  </div>
</template>
<script>
// import { ref } from 'vue'
// const textarea = ref('')
export default {
  data() {
    return {textarea:''}
  },
  methods: {
    send() {
      const api = "https://keimui43t1.execute-api.us-east-1.amazonaws.com/feedback";
      const data = {'msg': this.textarea}
      this.$axios
          .post(api, data)
          .then(res => {
            if (res.data.code == '001') {
              alert("Your feedback sent to us successfully!")
            }else{
              alert("Fail to send. Don't send empty contents.")
            }
          })
    }
  }
}
</script>
<!--<script>-->
<!--import MyMarkdown from "../components/MyMarkdown";-->
<!--export default {-->
<!--  components: {-->
<!--    MyMarkdown-->
<!--  }-->
<!--};-->
<!--</script>-->
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
