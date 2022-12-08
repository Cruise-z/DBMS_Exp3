<template>

   <Header/>
    <div class= "common-layout">
        <!-- <el-header><Header dropdown1="浏览商品" dropdown2="个人信息"/></el-header> -->
        <el-container>
          <el-main style="height  : calc(100vh - 50px)">
            <!-- 搜索区 -->
            <div style="display : flex;margin : 7px 0px;text-align: center;font-family: YouYuan">
              <span style="margin : 0px 10px;">价格区间:</span>
              <el-input v-model="SelectPrice.price_begin" placeholder="最低价" clearable :prefix-icon="Search" style="width : 10%"/>
              <span style="margin : 0px 10px;">-</span>
              <el-input v-model="SelectPrice.price_end" placeholder="最高价" clearable :prefix-icon="Search" style="width : 10%"/>
              <span style="margin : 0px 3% 0px 3%;"></span>
              <span style="margin : 0px 10px;">评分区间:</span>
              <el-input v-model="SelectScore.score_begin" placeholder="最低评分" clearable :prefix-icon="Search" style="width : 10%"/>
              <span style="margin : 0px 10px;">-</span>
              <el-input v-model="SelectScore.score_end" placeholder="最高评分" clearable :prefix-icon="Search" style="width : 10%"/>
              <span style="margin : 0px 3% 0px 3%;"></span>
              <el-select v-model="SelectPress" placeholder="筛选出版社" setsize="large" clearable style="15%">
                <el-option 
                  v-for="item in SelectOption"
                  :key="item.PressValue"
                  :value="item.PressValue"
                  :label="item.Presslabel"
                />
                </el-select>
                <span style="margin : 0px 1% 0px 1%;"></span>
                <el-input v-model="SelectAuthor" placeholder="输入作者全名" clearable style="width : 15%"/>
              
            </div>
            <div style="display : flex;">
              <el-button type="info" round style="margin : 2px 10px" @click="SearchMethod">搜索</el-button>
              <span style="margin : 0px 3% 0px 3%;"></span>
              <el-button type="info" round style="margin : 2px 10px" @click="AddBook">新增</el-button>
            </div>
            <!-- 展示区 -->
            <el-scrollbar style="height : 100% ">
            <el-table :data="tableData" border:true stripe style="width: 100%;height : calc(100vh - 70px); font-family : YouYuan;font-size : 20px;">
                    <el-table-column type="expand" >
                    <template #default="props">
                      <el-card class="box-card" style="width : 60%;margin : 0 20% 0 20%;">
                        <template #header >
                          <div class="card-header">
                            <span>更多细节</span>
                          </div>
                        </template>
                        <div class="text item"> 作者 : {{ props.row.author }}</div>
                        <div class="text item"> 出版社 : {{ props.row.press }}</div>
                        <div class="text item"> 价格 : {{ props.row.price }}</div>
                        <div class="text item"> 评分 : {{ props.row.score }}</div>
                      </el-card>
                    </template>
                    </el-table-column>
                    <el-table-column label="ISBN" prop="ISBN" sortable resizable />
                    <el-table-column label="书名" prop="title" resizable style="font-family : YouYuan;font-size : 20px;"/>
                    <el-table-column fixed="right" label="Operations">
                      <template #default="scope" style="font-family : YouYuan;font-size : 10px;">
                        <el-button link type="sucess" plain round size="middle" @click="RemarkShow(scope.row.ISBN,scope.row.title)">查看评论</el-button>
                        <el-popconfirm
                        confirm-button-text="是"
                        cancel-button-text="否"
                        title="确认删除？"
                        @confirm="confirmEvent(scope.row.ISBN)"
                        @cancel="cancelEvent"
                        >
                        <template #reference>
                          <el-button>Delete</el-button>
                        </template>
                        </el-popconfirm>
                        <el-button link type="sucess" plain round size="middle" @click="showMarkDialog(scope.row.ISBN,scope.row.title)">评分</el-button>
                      </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
          </el-main>
        </el-container>

        <!-- 弹窗 -->
        <el-dialog
        v-model="dialogVisible"
        title="书籍信息"
        width="30%"
        >
        <el-form :model="form" label-width="120px">
          <el-form-item label="ISBN">
            <el-input v-model="form.ISBN"></el-input>
          </el-form-item>
          <el-form-item label="书名">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <el-form-item label="作者">
            <el-input v-model="form.author"></el-input>
          </el-form-item>
          <el-form-item label="出版社">
            <el-input v-model="form.press"></el-input>
          </el-form-item>
          <el-form-item label="价格">
            <el-input v-model="form.price"></el-input>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="SaveBook">
              确认
            </el-button>
          </span>
        </template>
      </el-dialog>
      <!-- 评分弹窗 -->
      <el-dialog
      v-model="rateVisible"
      title="评分"
      width="50%"
      >
        <el-rate v-model="rate" show-text :texts="['oops', 'disappointed', 'normal', 'good', 'great']" allow-half />
        <br /> <br />
        <el-button type="primary" @click="markBook">
          确认
        </el-button>
      </el-dialog>
      <!-- 评论弹窗 -->
      <el-dialog
      v-model="RemarkVisible"
      :title="RemarkShowing.title +'评论'"
      width="90%"
      >
      <el-button type="success" @click="RemarkAddShow">评论书籍</el-button>
      <br/>
      <span style="margin : 3px 0px 10px 0px;"/>
      <el-scrollbar>
      <el-table :data="RemarkData" border:false stripe style="width: 100%;height : calc(90vh - 70px)">
        <el-table-column label="评论者" prop="name" sortable />
        <el-table-column label="评论时间" prop="time" sortable />
        <el-table-column label="内容" prop="comtent" />
        <el-table-column label="分数" prop="score" />
        <el-table-column fixed="right" label="Operations">
          <template #default="scope">
          <el-popconfirm
          confirm-button-text="是"
          cancel-button-text="否"
          title="确认删除？"
          @confirm="RemarkconfirmDelete(scope.row.name,scope.row.time)"
          @cancel="RemarkcancelDelete"
          >
            <template #reference>
              <el-button>删除</el-button>
            </template>
          </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      </el-scrollbar>
      </el-dialog>
      <!-- 新增评论弹窗 -->
      <el-dialog
      v-model="RemarkAddVisible"
      title="添加评论"
      width="40%">
      <el-input
        v-model="RemarkAddForm.content"
        :autosize="{ minRows: 4, maxRows: 5 }"
        maxlength="200"
        placeholder="Please input"
        show-word-limit
        type="textarea"
      />
      <template #footer>
          <span class="dialog-footer">
            <el-button @click="RemarkSaveCancle">取消</el-button>
            <el-button type="primary" @click="SaveRemark">
              确认
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
</template>

<style scoped>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: calc(100vh - 50px);
  }
  .layout-container-demo .el-main {
    padding: 0;
  }
  .layout-container-demo .toolbar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    right: 20px;
  }
  .el-scrollbar_wrap{
    overflow-x : hidden;
  }
  .card-header {
    justify-content: space-between;
    align-items: center;
    text-align: center;
    font-family: YouYuan;
    font-size: 17px;
  }

.text {
    font-size: 14px;
  }

.item {
    margin-bottom: 18px;
    text-align: center;
}

.box-card {
  width: 480px;
}
</style>
<script >


import request from '@/utils/request'
import Header from '@/components/Header.vue'
import Menu from '@/components/Menu.vue'
import  {Search} from '@element-plus/icons-vue'
export default{
    name : 'ViewPage',

    components : {
        Header ,
        Menu ,
        Search
    },

    data () {
      return {
        Search : Search,
        SelectOption : [
          {
            PressValue : "人民文学出版社",
            Presslabel : "人民文学出版社"
          },
          {
            PressValue : "广西师范大学出版社",
            Presslabel : "广西师范大学出版社"
          },
          {
            PressValue : "北京联合出版社公司",
            Presslabel : "北京联合出版社公司"
          },
          {
            PressValue : "上海译文出版社",
            Presslabel : "上海译文出版社"
          },
          {
            PressValue : "上海人民出版社",
            Presslabel : "上海人民出版社"
          },
          {
            PressValue : "新星出版社",
            Presslabel : "新星出版社"
          },
          {
            PressValue : "上海文艺出版社",
            Presslabel : "上海文艺出版社"
          }
        ],
        SelectPress : "",
        SelectAuthor : "",
        SelectPrice : {
          price_begin : -1,
          price_end : -1
        },
         SelectScore : {
          score_begin : -1,
          score_end : -1
        },
        form : {},
        dialogVisible : false,
        rateVisible : false,
        rate: 0,
        tableData : [
          {
            ISBN : "111",
            title : "",
            author : "",
            press : "",
            price : "",
            score : 0.0
          }
        ],
        RemarkVisible : false,
        RemarkShowing : {
          ISBN : "",
          title : ""
        }, // 记录正在展示评论的书的ISBN和书名
        rateShowing : {
          ISBN : "",
          title : ""
        },
        RemarkData : [
          {
            name :"",
            time : "",
            content : "",
            score : ""
          }
        ],
        RemarkAddVisible : false,
        RemarkAddForm : {
          content : ""
        }
      }
    },

    created : function(){
        this.load()
    },
    
    methods : {
      handleClick : function(){
        alert("!!!");
      },
      confirmEvent : function(ISBN){
        request.post("bookweb/deleteBook",{
          ISBN: ISBN
        }).then(
          res => {
            if(res.status_code == 0){
              alert("删除成功!");
              this.load();
            }
          }
        )
      },
       AddBook : function(){
        
        this.dialogVisible = true;
        this.form = {};
      },
      SaveBook : function(){
        request.post("bookweb/addBook",{
          ISBN: this.form.ISBN,
          title: this.form.title,
          author: this.form.author,
          press: this.form.press,
          price: this.form.price
        }).then(res => {
          console.log(res);
          if(res.status_code == 0){
            alert("上传成功！");
            this.dialogVisible = false;
          }
        });
      },
      showMarkDialog : function(ISBN,title){
        this.rateShowing = {
          ISBN : ISBN,
          title : title
        };
        this.rateVisible = true;
      },
      markBook : function(){
        // alert("你的评分："+this.rate*2+"已提交！");
        request.post("bookweb/mark", {
          ISBN: this.rateShowing.ISBN,
          score: this.rate*2,
        }).then(
          res => {
            if(res.status_code == 0){
              alert("数据库更新成功");
              this.rateVisible=false;
              this.rateShowing = {
                ISBN : "",
                title : ""
              }
            }
          }
        )
      },
      load : function(){
        console.log(this.SelectPress);
        var String 
        request.post("bookweb/userBook",{
          press : this.SelectPress,
          author : this.SelectAuthor,
          score_range : {
            score_begin : this.SelectScore.score_begin,
            score_end : this.SelectScore.score_end
          },
          price_range : {
            price_begin : this.SelectPrice.price_begin,
            price_end : this.SelectPrice.price_end
          }
        }).then(
          res=>{
            console.log(res);
            this.tableData = res.books_dict
          }
        );
      },
      SearchMethod : function(){
        this.load();
        this.SelectPrice = {
          price_begin : -1,
          price_end : -1
        };
        this.SelectScore = {
          score_begin : -1,
          score_end : -1
        };
        this.SelectPress = "";
        this.SelectAuthor = "";
      },
      RemarkShow : function(ISBN,title){
        this.RemarkShowing = {
          ISBN : ISBN,
          title : title
        }
        this.RemarkVisible = true;
        request.post("bookweb/viewRemark",{
          ISBN : this.RemarkShowing.ISBN
        }).then(
          res => {
            console.log(res.remarks_dict);
            this.RemarkData = res.remarks_dict
          }
        );
      },
      RemarkconfirmDelete : function(name,time){
        request.post("bookweb.deleteComment",{
          ISBN : this.RemarkShowing.ISBN,
          username : name,
          timeStamp : time
        }).then(
          res => {
            if (res.status_code == 0){
              alert("删除成功！");
              //重新渲染
              this.RemarkShow(this.RemarkShowing.ISBN,this.RemarkShowing.title);
            }else{
              alert("删除失败，权限不够！");
            }
          }
        );
      },
      RemarkAddShow : function(){
        this.RemarkAddVisible = true;
      },
      SaveRemark : function(){
        request.post("bookweb/comment",{
          ISBN : this.RemarkShowing.ISBN,
          content : this.RemarkAddForm.content
        }).then(
          res => {
            if (res.status_code == 200){
              alert("感谢您的评论！");
              // this.RemarkAddForm = {
              //   content : ""
              // }
            }
          }
        )
      },
      RemarkSaveCancle : function(){
        this.RemarkAddForm = {
          content : ""
        };
        this.RemarkAddVisible = false;
      }
    }
}



</script>
