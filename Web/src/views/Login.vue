<template>
  <div class="main">
      <!-- 背景 -->
    <particles></particles>
    <!-- 主体 -->
    <div class="Loginmain" style="background-color: rgba(255, 0, 0, 0);">
    <el-form class= "Login-Form" :model="LoginForm" label-width="120px" >
        <h2 >登  录</h2>
        <el-form-item class="Login-Input" label='用户名'>
            <el-input v-model="LoginForm.Name" clearable placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item class="Login-Input" label='密码'>
            <el-input v-model="LoginForm.Password" clearable show-password placeholder="密码"></el-input>
        </el-form-item>
        <el-form-item >
            <el-button class="Login-Button" round dark color="rgba(164, 211, 214, 0.609)" @click="LoginOP">登录</el-button>
            <el-button class="Login-Button" round dark color="rgba(164, 211, 214, 0.609)" @click="RegisterShow">注册</el-button>
        </el-form-item>
    </el-form>
    </div>

    <!-- 注册表单 -->
    <el-dialog width="25%" title="用户注册" v-model="dialogVisible">
        <el-form :model="RegisterForm" label-width="120px">
            <el-form-item label="用户名">
                <el-input v-model="RegisterForm.name" clearable placeholder="用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码">
                <el-input v-model="RegisterForm.password" clearable show-password placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item label="电话">
                <el-input v-model="RegisterForm.telephone" clearable placeholder="电话"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
                <el-input v-model="RegisterForm.email" clearable placeholder="邮箱"></el-input>
            </el-form-item>
            <el-form-item label="城市">
                <el-input v-model="RegisterForm.city" clearable placeholder="城市"></el-input>
            </el-form-item>
            <el-form-item label="性别">
                <el-switch v-model="RegisterForm.Ismale" 
                active-color="rgba(192, 237, 245, 0.97)"
                active-text="男" 
                inactive-color="rgba(192, 237, 245, 0.4)"
                inactive-text="女"/>
            </el-form-item>
            <el-form-item label="注册类型">
                <el-switch v-model="RegisterForm.Isuser" 
                active-color="rgba(192, 237, 245, 0.97)"
                active-text="用户" 
                inactive-color="rgba(192, 237, 245, 0.4)"
                inactive-text="管理员"/>
            </el-form-item>
        </el-form>
        <el-button type="failed" color="rgba(192, 237, 245, 0.92)" @click="RegisterCancle">取消</el-button>
        <el-button type="primary" color="rgba(191, 236, 245, 0.92)" @click="RegisterCommit">注册</el-button>
    </el-dialog>
  </div>
</template>

<style scoped>
    .Loginmain{
        margin: 10% 25% 15% 25%;
        /* border: 3px solid #000; */
    }
    .Login-Form{
        border-radius: 40px;
        background-clip: padding-box;
        margin: 70px auto;
        width:500px;
        height: 500px;
        background: rgba(32, 39, 38, 0.466);
        border:2px inset rgba(207, 238, 238, 0.739);
        text-align: center;
        font-size: 28px;
        font-family: YouYuan;
        color: rgba(191, 211, 218, 0.794);
    }
    .Login-Input{
        width: 80%;
        margin: 50px 10px 70px 20px;
        /* border: 2px solid #000; */
        font-size: 20px;
    }
    .Login-Button{
        width : 30%;
        
    }

</style>
    
<script>
import Particles from '@/components/index.vue'
import request from '@/utils/request'
    export default{
        name : "Login",
        components : {
            Particles : Particles
        },
        data (){
            return {
                LoginForm : {
                    Name : "",
                    Password : ""
                },
                dialogVisible : false,
                RegisterForm : {
                    name : "",
                    password : "",
                    telephone : "",
                    email : "",
                    city : "",
                    Ismale : true,
                    Isuser : true
                }
            }
        },
        methods : {
            // 实现登录，并跳转页面
            LoginOP : function(){
                //判断用户密码不为空
                if(this.LoginForm == {} || this.LoginForm.Name == '' || this.LoginForm.Password== ''){
                    alert("请输入用户名或密码");
                }else{    //不为空则向后端传递数据
                    console.log(this.LoginForm)
                    request.post("/bookweb/login",{
                        name : this.LoginForm.Name,
                        password : this.LoginForm.Password,
                        form : this.RegisterForm,
                        form2 :{
                            "a" : "a",
                            "b" : "b"
                        }
                    }).then(
                        res =>{
                            console.log(res);
                            //登录成功跳转页面
                            if(res.status_code == 200){
                                alert("登录成功！");
                                this.$router.push({path:"/View"}) //页面跳转
                            }else if (res.status_code == 404){
                                alert("用户未注册，请注册用户！");
                            }else{
                                alert("密码错误！");
                            }
                        }
                    )
                }
            },
            RegisterShow : function(){
                console.log(this.dialogVisible)
                this.dialogVisible = true;
                this.RegisterForm = {
                    name : "",
                    password : "",
                    telephone : "",
                    email : "",
                    city : "",
                    Ismale : true,
                    Isuser : true
                }
            },
            RegisterCancle : function(){
                this.RegisterForm = {
                    name : "",
                    password : "",
                    telephone : "",
                    email : "",
                    city : "",
                    Ismale : true,
                    Isuser : true
                };
                this.dialogVisible = false;
            },
            RegisterCommit : function(){
                //post提交，后台允许后返回值，然后弹窗注册成功
                if (this.RegisterForm.Name=="" || this.RegisterForm.Password==""){
                    alert("请输入完整信息");
                }else{
                    request.post("/bookweb/register",this.RegisterForm).then(
                        res => {
                            if(res.data.status_code == 401){
                                alert("该用户已存在");
                            }else if(res.data.status_code == 404){
                                alert("密码非法");
                            }else if(res.data.status_code == 200){
                                alert("注册成功,你可以登录啦！");
                            }
                        }
                    );
                }
            }
        }
    }
</script>

