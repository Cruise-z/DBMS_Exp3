<template>
    <header>
        <div id="header_logo"><img src="../assets/book_logo.svg" style="width: 190px;height : 100%" /></div>
        <div style="flex : 1"></div>
        <div id="header_person">
            <el-button @click="Logout">
                <el-icon :size="20"><Edit /></el-icon> 注销
            </el-button>
            <el-button @click="GoToBook">
                <el-icon :size="20"><HomeFilled /></el-icon> 主页
            </el-button>
            <el-button @click="GoToPrivate">
                <el-icon :size="20"><UserFilled /></el-icon> 个人
            </el-button>
        </div>
    </header>
</template>

<style scoped>
header {
    height: 50px;
    width: 100%;
    border-bottom: 2px solid #e7d092;
    background-color: #54749485;
    display: flex;
    padding: 3px;
    margin: 2px;
    align-items: center;
}

#header_logo {
    /* width: 120px; */
    text-align: center;
    margin-top: 20px;
}

#header_person {
    width: 300px;

}

.example-showcase .el-dropdown-link {
    cursor: pointer;
    color: var(--el-color-primary);
    display: flex;
    align-items: center;
}

.flex-grow {
    flex-grow: 1;
}
</style>

<script >
import request from '@/utils/request';
import {
    Edit,
    HomeFilled,
    Message,
    Star,
    UserFilled
} from '@element-plus/icons-vue';
export default {
    name: 'Header',
    components: {
    Edit,
    Message,
    Star,
    HomeFilled,
    UserFilled
},
    methods: {
        GoToBook: function () {
            this.$router.push({ path: "/View" });
        },
        GoToPrivate: function () {
            this.$router.push({ path: "/Private" });
        },
        Logout: function () {
            request.post("/bookweb/logout", {}).then(
                res => {
                    if (res.status_code == 200) {
                        alter("注销成功！");
                        this.$router.push({path : "/"});
                        
                    } else {
                        alert("出错！");
                    }
                }
            )
        }
    }
}
</script>

