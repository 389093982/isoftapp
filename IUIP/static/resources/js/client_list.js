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
        $('#appids-table').bootstrapTable({
            url: '/resources/loadClientsData/',           //请求后台的URL（*）
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
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'client_name',
                title: 'client_name',
                sortable : true
            }, {
                field: 'client_short_name',
                title: 'client_short_name',
                sortable : true
            }, {
                field: 'created_by',
                title: 'created_by'
            },  {
                field: 'created_date',
                title: 'created_date'
            },  {
                field: 'last_updated_by',
                title: 'last_updated_by'
            },  {
                field: 'last_updated_date',
                title: 'last_updated_date'
            }, {
                field: 'operate',
                title: '操作',
                align: 'center',
                valign: 'middle',
                formatter: operateFormatter //自定义方法，添加操作按钮
            },]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            client_name: $("#txt_search_client_name").val(),
            client_short_name: $("#txt_search_client_short_name").val(),
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
            $('#appids-table').bootstrapTable('refresh');
        });

        $('#btn_edit').click(function(){
            editItems($('#appids-table'), "/appmanager/edit/");
        });

        $('#btn_add').click(function(){
            window.location="/appmanager/appid_add/";
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

function operateFormatter(value, row, index) {//赋予的参数
    var href = "/resources/resources_list/?client_short_name=" + row.client_short_name;
    return '<a href="' + href + '" title="查看相关子项信息"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>';
}