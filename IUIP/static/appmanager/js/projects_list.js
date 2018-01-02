//$(function () {
//    //1.初始化Table
//    var oTable = new TableInit();
//    oTable.Init();
//    //2.初始化Button的点击事件
//    var oButtonInit = new ButtonInit();
//    oButtonInit.Init();
//
//    $('#btn_reset').click(function(){
//        $('#formSearch')[0].reset();
//    });
//});
//
//
//var TableInit = function () {
//    var oTableInit = new Object();
//    //初始化Table
//    oTableInit.Init = function () {
//        $('#appids-table').bootstrapTable({
//            url: '/appmanager/loadProjectsData/',           //请求后台的URL（*）
//            method: 'get',                      //请求方式（*）
//            toolbar: '#toolbar',                //工具按钮用哪个容器
//            striped: true,                      //是否显示行间隔色
//            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
//            pagination: true,                   //是否显示分页（*）
//            sortable: true,                     //是否启用排序
//            sortOrder: "asc",                   //排序方式
//            queryParams: oTableInit.queryParams,//传递参数（*）
//            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
//            pageNumber:1,                       //初始化加载第一页，默认第一页
//            pageSize: 10,                       //每页的记录行数（*）
//            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
//            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
//            strictSearch: true,
//            showColumns: true,                  //是否显示所有的列
//            showRefresh: true,                  //是否显示刷新按钮
//            minimumCountColumns: 2,             //最少允许的列数
//            clickToSelect: true,                //是否启用点击选中行
//            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
//            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
//            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
//            cardView: false,                    //是否显示详细视图
//            detailView: false,                   //是否显示父子表
//            columns: [{
//                checkbox: true
//            }, {
//                field: 'project_id',
//                title: 'project_id',
//                sortable : true
//            }, {
//                field: 'project_name',
//                title: 'project_name',
//                sortable : true
//            }, {
//                field: 'project_appid',
//                title: 'project_appid',
//                align : 'center',
//                sortable : true
//            }, {
//                field: 'created_by',
//                title: 'created_by'
//            },  {
//                field: 'created_date',
//                title: 'created_date'
//            },  {
//                field: 'last_updated_by',
//                title: 'last_updated_by'
//            },  {
//                field: 'last_updated_date',
//                title: 'last_updated_date'
//            }, {
//                field: 'operate',
//                title: '操作',
//                align: 'center',
//                valign: 'middle',
//                formatter: operateFormatter //自定义方法，添加操作按钮
//            },],
//        });
//    };
//
//    //得到查询的参数
//    oTableInit.queryParams = function (params) {
//        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
//            limit: params.limit,   //页面大小
//            offset: params.offset,  //页码
//            project_id: $("#txt_search_project_id").val(),
//            project_name: $("#txt_search_project_name").val(),
//            project_appid: $("#txt_search_project_appid").val(),
//            search: params.search,      //搜索
//            sortOrder: params.order,    //排序
//            sortName:params.sort        //排序字段
//        };
//        return temp;
//    };
//    return oTableInit;
//};
//
//
//var ButtonInit = function () {
//    var oInit = new Object();
//    var postdata = {};
//
//    oInit.Init = function () {
//        //初始化页面上面的按钮事件
//        $('#btn_query').click(function(){
//            $('#appids-table').bootstrapTable('refresh');
//        });
//
//        $('#btn_edit').click(function(){
//            editItems($('#appids-table'), "/appmanager/edit/");
//        });
//
//        $('#btn_add').click(function(){
//            window.location="/appmanager/add/";
//        });
//    };
//
//    return oInit;
//};
//
//function editItems($table, requestUrl){
//    var selRow = $table.bootstrapTable('getSelections');
//    if(selRow != null && selRow.length == 1){
//        window.location="/appmanager/edit/" + selRow[0].app_id;
//    }else{
//        alert('一次只能操作一行!');
//    }
//}
//
//function operateFormatter(value, row, index) {//赋予的参数
//    var href = "/appmanager/projects/?app_id=" + row.app_id;
//    return '<a href="' + href + '" title="查看集成点"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>';
//}

$(function(){
    $("#projects-table").datagrid({
       title:"项目管理",
       width:900,
        height:500,
        url:"/appmanager/loadProjectsData/",
        fitColumns:true,
        striped:true,
        queryParams:{},
        fit:true,
        columns:[[{
            field:'ck',
            checkbox:true
        },{
            field:"project_id",
            title:"project_id",
            width:100,
            sortable:true
        },{
            field:"project_name",
            title:"project_name",
            width:100,
            sortable:true
        },{
            field:"project_appid",
            title:"project_appid",
            width:100,
            sortable:true
        },{
            field:"created_by",
            title:"created_by",
            width:100
        },{
            field:"last_updated_by",
            title:"last_updated_by",
            width:100
        },{
            field:"last_updated_date",
            title:"last_updated_date",
            width:100
        },{
            field:"operate",
            title:"operate",
            formatter:operateFormatter,
            width:100
        }]],
        pagination:true,
        pageSize:10,
        pageList:[10,15,20,50,100]
    });

    bindHrefEvent();
})

function bindHrefEvent(){
    $("#btn_query").click(function(){
        //查询参数直接添加在queryParams中
        var queryParams = $("#projects-table").datagrid('options').queryParams;

        queryParams.csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        queryParams.project_id = $("input[name='project_id']").val();
        queryParams.project_name = $("input[name='project_name']").val();
        queryParams.project_appid = $("input[name='project_appid']").val();

        $("#projects-table").datagrid('options').queryParams=queryParams;

        //重新加载datagrid的数据
        $("#projects-table").datagrid('reload');
    });

    $("#btn_reset").click(function(){
        $("#formSearch").form('clear');
    });
}

function operateFormatter(val,row,index){
    var html = '<a href="/appmanager/project_add/">添加</a>&nbsp;'
             + '<a href="/appmanager/project_edit/?project_id=' + row.project_id + '">编辑</a>&nbsp;'
             + '<a href="#" title="/appmanager/project_delete/?project_id=' + row.project_id + '" onclick="project_delete(this)">删除</a>';
    return html;
}

function project_delete(aNode){
    $.messager.confirm('删除操作', '确认要删除么 ?', function(r){
        if (r){
            $.ajax({
                type: "GET",
                url: aNode.title,
                success: function(data){
                    var obj = JSON.parse(data);
                    if(obj.status == 'SUCCESS'){
                        //重新加载datagrid的数据
                        $("#appids-table").datagrid('reload');
                    }
                    $.messager.show({
                        title:obj.status,
                        msg:obj.msg
                    });
                }
            });
        }
    });
}
