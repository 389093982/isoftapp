$(function(){
    $("#appids-table").datagrid({
       title:"应用管理",
       width:900,
        height:500,
        url:"/appmanager/loadAppIdsData/",
        fitColumns:true,
        striped:true,
        queryParams:{},
        fit:true,
        columns:[[{
            field:'ck',
            checkbox:true
        },{
            field:"app_id",
            title:"app_id",
            width:100,
            sortable:true
        },{
            field:"app_name",
            title:"app_name",
            width:100,
            sortable:true
        },{
            field:"app_owner",
            title:"app_owner",
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
        var queryParams = $("#appids-table").datagrid('options').queryParams;

        queryParams.csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        queryParams.app_id = $("input[name='app_id']").val();
        queryParams.app_name = $("input[name='app_name']").val();
        queryParams.app_owner = $("input[name='app_owner']").val();

        $("#appids-table").datagrid('options').queryParams=queryParams;

        //重新加载datagrid的数据
        $("#appids-table").datagrid('reload');
    });

    $("#btn_reset").click(function(){
        $("#formSearch").form('clear');
    });
}

function operateFormatter(val,row,index){
    var html = '<a href="/appmanager/appid_edit/">添加</a>&nbsp;'
             + '<a href="/appmanager/appid_edit/?app_id=' + row.app_id + '">编辑</a>&nbsp;'
             + '<a href="#" title="/appmanager/appid_delete/?app_id=' + row.app_id + '" onclick="appid_delete(this)">删除</a>';
    return html;
}

function appid_delete(aNode){
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


