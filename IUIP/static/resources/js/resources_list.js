$(function () {
    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();
    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

    $('#btn_reset').click(function(){
        $('#formSearch')[0].reset();
    });
});


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#resources-table').bootstrapTable({
            url: '/resources/loadResourcesData/',           //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "id",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            },
//            {
//                field: 'id',
//                title: '序号'
//            },
            {
                field: 'resource_name',
                title: 'resource_name',
            }, {
                field: 'resource_url',
                title: 'resource_url',
                width:10,
            }, {
                field: 'resource_username',
                title: 'resource_username'
            },  {
                field: 'resource_password',
                title: 'resource_password'
            },  {
                field: 'resource_type',
                title: 'resource_type'
            },  {
                field: 'env_name',
                title: 'env_name'
            },  {
                field: 'client_short_name',
                title: 'client_short_name'
            },  {
                field: 'connection_test',
                title: '测试状态',
                align : 'center',
                formatter: function(value, row, index) {
                    if(value == "SUCCESS"){
                        return "<font color='#009900'>" + value + "</font>";
                    }else if(value.indexOf("ERROR") > 0){
                        return "<font color='#FF0000'>" + value + "</font>";
                    }else{
                        return value;
                    }
                }
            },],
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            resource_name: $("#txt_search_resource_name").val(),
            resource_client: $("#txt_search_resource_client").val(),
            search: params.search,      //搜索
            sortOrder: params.order,    //排序
            sortName:params.sort        //排序字段
        };
        return temp;
    };
    return oTableInit;
};


var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
        $('#btn_query').click(function(){
            $('#resources-table').bootstrapTable('refresh');
        });

        $('#btn_edit').click(function(){
            editItems($('#appids-table'), "/appmanager/edit/");
        });

        $('#btn_add').click(function(){
            window.location="/appmanager/add/";
        });

        $('#btn_connection_test').click(function(){
            connectionTest();
        });
    };
    return oInit;
};

function editItems($table, requestUrl){
    var selRow = $table.bootstrapTable('getSelections');
    if(selRow != null && selRow.length == 1){
        window.location="/appmanager/edit/" + selRow[0].app_id;
    }else{
        alert('一次只能操作一行!');
    }
}

function updateCellForConnectionTest(index,value){
    $('#resources-table').bootstrapTable('updateCell', {
        index : index,
        field: 'connection_test',
        value: value
    });
}

function connectionTest(){
    // 显示加载图标
    showLoadIcon();
    // 循环发送请求
    __connectionTest__();
}

// 显示加载图标
function showLoadIcon(){
    var selections = $('#resources-table').bootstrapTable('getSelections');
    for(var i=0; i<selections.length; i++){
        var selection = selections[i];
        updateCellForConnectionTest(selection.id,'<img src="/static/common/img/Loading2.gif" width="20" height="20">');
    }
}

// 创建 Ajax 对象
function creatXMLHttpRequest() {
    var xmlHttp;
    if (window.ActiveXObject) {
        return xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        return xmlHttp = new XMLHttpRequest();
    }
}

function __connectionTest__(){
    // 发送请求
    var selections = $('#resources-table').bootstrapTable('getSelections');
    for(var i=0; i<selections.length; i++){
        var selection = selections[i];
        var resource_type = selection.resource_type;
        var resource_url = selection.resource_url;
        var resource_username = selection.resource_username;
        var resource_password = selection.resource_password;

        $.ajax({
            type:"POST",
            async: false,
            url:"/resources/connectionTest/",
            data:{"dbType":resource_type,"url":resource_url,
                "username":resource_username,"password":resource_password},
            datatype: "jsonp",
            success:function(data){
                if(data.status == 'SUCCESS'){
                    updateCellForConnectionTest(selection.id,"<font color='#009900'>SUCCESS</font>");
                }else{
                    updateCellForConnectionTest(selection.id,"<font style='color:#FF0000'>ERROR<br>" + data.result + "</font>");
                }
            },
        });
    }
}