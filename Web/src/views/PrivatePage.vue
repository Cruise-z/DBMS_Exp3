<template>
    <Header dropdown1="浏览商品" dropdown2="个人信息" />
    <div id="back">
        <!-- 个人信息 -->
        <el-descriptions class="info_card card" title="个人信息" :column="1">
            <el-descriptions-item>
                <!-- 头像 -->
                <div style="text-align: center;">
                    <el-upload action="#" list-type="picture-card" limit=1 :auto-upload="false" :file-list="head"
                        :class="{ hide: hideUpload }" :on-preview="handlePictureCardPreview" :on-remove="handleRemove"
                        :on-change="handleChange">
                        <el-icon>
                            <Plus />
                        </el-icon>
                    </el-upload>
                    <el-dialog v-model="dialogVisible">
                        <img w-full :src="dialogImageUrl" alt="Preview Image" />
                    </el-dialog>
                </div>
                <br />
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <el-icon>
                        <User />
                    </el-icon>
                    用户名
                </template>
                <div class="info">{{ privateInfo.username }}</div>
                <hr />
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <el-icon>
                        <Avatar />
                    </el-icon>
                    用户ID
                </template>
                <div class="info">{{ privateInfo.userID }}</div>
                <hr />
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <el-icon>
                        <Iphone />
                    </el-icon>
                    电话
                </template>
                <div class="info">{{ privateInfo.telephone }}</div>
                <hr />
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <el-icon>
                        <Message />
                    </el-icon>
                    邮箱
                </template>
                <div class="info">{{ privateInfo.email }}</div>
                <hr />
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <el-icon>
                        <Location />
                    </el-icon>
                    城市
                </template>
                <div class="info">{{ privateInfo.city }}</div>
                <hr />
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <el-icon>
                        <UserFilled />
                    </el-icon>
                    用户类型
                </template>
                <div class="info"><el-tag>{{ privateInfo.authType }}</el-tag></div>
                <hr />
            </el-descriptions-item>
        </el-descriptions>
        <!-- 修改信息 -->
        <div class="card change_card">
            <h3>修改信息</h3>
            <el-tabs v-model="activeName" @tab-click="handleClick">
                <!-- 修改基本资料 -->
                <el-tab-pane label="基本资料" name="first">
                    <el-form :model="form" label-width="120px">
                        <el-form-item label="用户名">
                            <el-input v-model="form.username" />
                        </el-form-item>
                        <el-form-item label="电话">
                            <el-input v-model="form.telephone" />
                        </el-form-item>
                        <el-form-item label="邮箱">
                            <el-input v-model="form.email" />
                        </el-form-item>
                        <el-form-item label="城市">
                            <el-input v-model="form.city" />
                        </el-form-item>
                        <el-form-item label="性别">
                            <el-radio-group v-model="form.sex">
                                <el-radio label="男" size="large">男</el-radio>
                                <el-radio label="女" size="large">女</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="submit_info">保存</el-button>
                            <el-button type="primary" @click="reset_info">重置</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
                <!-- 修改密码 -->
                <el-tab-pane label="修改密码" name="second">
                    <el-form :model="passForm" status-icon label-width="120px" :rules="rules" ref="passForm"
                        class="demo-passForm">
                        <el-form-item label="原密码" prop="originPass">
                            <el-input v-model="passForm.originPass" type="password" autocomplete="off" />
                        </el-form-item>
                        <el-form-item label="新密码" prop="newPass">
                            <el-input v-model="passForm.newPass" type="password" autocomplete="off" />
                        </el-form-item>
                        <el-form-item label="确认密码" prop="checkPass">
                            <el-input v-model="passForm.checkPass" type="password" autocomplete="off" />
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="submitPass">提交</el-button>
                            <el-button @click="resetPass">清空</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
            </el-tabs>

        </div>
    </div>

</template>

<script>
import request from '@/utils/request'
import Header from '@/components/Header.vue'
import reading from '../assets/reading.jpeg'
import { ref } from 'vue'
import {
    Plus,
    Iphone,
    Location,
    User,
    Avatar,
    Message,
    UserFilled,
} from '@element-plus/icons-vue'
import { assertTSAnyKeyword } from '@babel/types'


export default {
    name: 'PrivatePage',
    components: {
        Plus,
        Header,
        Iphone,
        Location,
        User,
        Avatar,
        Message,
        UserFilled
    },
    data() {
        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'));
            } else {
                if (this.passForm.checkPass !== '') {
                    this.$refs.passForm.validateField('checkPass');
                }
                callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.passForm.pass) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        };
        return {
            form: {
                username: '',
                telephone: '',
                sex: '',
                city: '',
                email: '',
            },
            imageUrl: reading,
            head: [{ name: 'default', url: reading }],
            privateInfo: {
                username: "张三",
                userID: "0001",
                telephone: "13000000000",
                email: "email@gail.com",
                city: "北京",
                authType: "管理员",
                sex: "女",
            },
            activeName: ref('first'),
            hideUpload: true,
            dialogImageUrl: ref(''),
            dialogVisible: ref(false),
            passForm: {
                originPass: '',
                newPass: '',
                checkPass: '',
            },
            rules: {
                originPass: [
                    { validator: validatePass, trigger: 'blur' }
                ],
                newPass: [
                    { validator: validatePass, trigger: 'blur' }
                ],
                checkPass: [
                    { validator: validatePass2, trigger: 'blur' }
                ],
            }
        }
    },
    created() {
        // this.load();
        this.reset_info()
    },
    methods: {
        load: function () {
            request.post("/bookweb/showInfo", {
            }).then(
                res => {
                    console.log(res);
                    this.privateInfo.username = res.info.username;
                    this.privateInfo.userID = res.info.ID;
                    this.privateInfo.email = res.info.email;
                    this.privateInfo.city = res.info.city;
                    this.privateInfo.authType = res.info.authType;
                    this.privateInfo.sex = res.info.sex;
                    this.privateInfo.telephone = res.info.telephone
                }
            );
        },
        submit_info: function () {
            request.post("/bookweb/updateInfo", {
                new_name: this.form.username,
                telephone: this.form.telephone,
                email: this.form.email,
                city: this.form.city,
                sex: this.form.sex
            }).then(
                res => {
                    console.log(res);
                    if(res.status_code == 200){
                        alert("修改成功！");
                        this.load();
                    }
                    else if(res.status_code == 404){
                        alert("更新失败！")
                    }
                    this.reset_info();
                }
            );
        },
        submitPass: function () {
            if (this.passForm.newPass == null || this.passForm.originPass == null || this.passForm.checkPass == null)
                alert("请输入完整！")
            else if (this.passForm.newPass != this.passForm.checkPass)
                alert("新密码与确认密码不一致！")
            else request.post("bookweb/updatePassword", {
                originPass: this.passForm.originPass,
                newPass: this.passForm.newPass
            }).then(
                res => {
                    console.log(res);
                    if(res.status_code==200){
                        alert("修改成功！");
                        this.resetPass();
                    }
                    else if(res.status_code==401){
                        alert("原密码错误！")
                        this.passForm.originPass = null;
                    }
                    else if(res.status_code==402){
                        alert("新密码不合法！")
                        this.resetPass();
                    }
                }
            )
        },
        resetPass: function () {
            this.passForm.originPass = null
            this.passForm.checkPass = null
            this.passForm.newPass = null
        },
        reset_info: function () {
            this.form.username = this.privateInfo.username
            this.form.telephone = this.privateInfo.telephone
            this.form.email = this.privateInfo.email
            this.form.city = this.privateInfo.city
            this.form.sex = this.privateInfo.sex
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
            this.hideUpload = !this.hideUpload;
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        handleChange() {
            this.hideUpload = !this.hideUpload;
        },
    }
}
</script>

<style scoped>
#back {
    background-color: #f2f2f2;
    height: calc(100vh - 70px);
    /* padding: 10px; */
}

.card {
    margin: 20px;
    padding: 20px;
    background-color: rgb(255, 255, 255);
    float: left;
    /* border-style: solid; */
    /* height: calc(100vh-10px); */
}

.info_card {
    width: 35%;
    /* float:left; */
}

.change_card {
    width: 55%;
    /* float:left; */
}

.el-icon {
    color: #409EFC;
}

.info {
    text-align: right;
    float: right;
}

.avatar {
    width: 178px;
    height: 178px;
    display: block;
}
</style>

<style lang="less" scoped>
/deep/.hide .el-upload--picture-card {
    display: none;
}
</style>

<style>
.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}
</style>