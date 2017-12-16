$(function () {
    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();
    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();
    // 默认隐藏列
    $('#intg_list_table').bootstrapTable('hideColumn', 'last_updated_date');

    $('#btn_reset').click(function(){
        $('#formSearch')[0].reset();
    });
});

var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#intg_list_table').bootstrapTable({
            url: '/timer/loadIntgsData/',           //请求后台的URL（*）
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
            height: 520,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
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
                field: 'integration_point_name',
                title: '集成点名称',
                formatter:function(value, row, index){
                        // 超链接无下划线,且鼠标悬停有提示
                        var html = "<a href='#' style='text-decoration:none' data-toggle='tooltip' title='" + value + "'>" + value + "</a>";
                        return html;
                    }
            }, {
                field: 'integration_point_version',
                title: '版本号',
            }, {
                field: 'env_name',
                title: '环境名称'
            },  {
                field: 'status',
                title: '状态',
                formatter: statusFormatter
            },  {
                field: 'source_client_name',
                title: '源系统'
            },  {
                field: 'target_client_name',
                title: '宿系统'
            },  {
                field: 'last_run_log',
                title: '最后一次运行状态',
                align: 'center',
                formatter: runLogFormatter
            }, {
                field: 'last_updated_date',
                title: '最后更新时间',
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
            integration_point_name: $("#txt_search_integration_point_name").val(),
            env_name: $("#txt_search_env_name").val(),
            source_client_name: $("#txt_search_source_client_name").val(),
            target_client_name: $("#txt_search_target_client_name").val(),
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
            $('#intg_list_table').bootstrapTable('refresh');
            // 绑定超链接事件
            bindHrefEvent();
        });
    };
    return oInit;
};

function operateFormatter(value, row, index) {//赋予的参数
    var status = row.status;
    var str = "";
    if(status == 0){
        // 草稿状态的集成点可编辑、可删除
        str = appendEditLink(str,row.integration_point_name,row.integration_point_version);
        str = appendDelLink(str,row.integration_point_name,row.integration_point_version);
    }else if(status == 1){
        str = appendEditLink(str,row.integration_point_name,row.integration_point_version);
        str = appendDeployLink(str,row.integration_point_name,row.integration_point_version);
        str = appendRunonceLink(str,row.integration_point_name,row.integration_point_version);
        str = appendDelLink(str,row.integration_point_name,row.integration_point_version);
    }else if(status == 2){
        str = appendStopLink(str,row.integration_point_name,row.integration_point_version);
        str = appendRunonceLink(str,row.integration_point_name,row.integration_point_version);
    }else if(status == 3){
        str = appendStartLink(str,row.integration_point_name,row.integration_point_version);
    }else{
        str = "";
    }
    return str;
}

function appendStartLink(str,integration_point_name,integration_point_version){
    var stophref = "/timer/intg/start?integration_point_name=" + integration_point_name
                    + "&integration_point_version=" + integration_point_version;
    str += '<a href="#" link="' + stophref + '" title="启用" onclick="intgStart(this)"><span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span></a>&nbsp;';
    return str;
}

function appendStopLink(str,integration_point_name,integration_point_version){
    var stophref = "/timer/intg/stop?integration_point_name=" + integration_point_name
                    + "&integration_point_version=" + integration_point_version;
    str += '<a href="#" link="' + stophref + '" title="停用" onclick="intgStop(this)"><span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span></a>&nbsp;';
    return str;
}

function appendDeployLink(str,integration_point_name,integration_point_version){
    var deloyhref = "/timer/intg/deploy?integration_point_name=" + integration_point_name
                    + "&integration_point_version=" + integration_point_version;
    str += '<a href="#" link="' + deloyhref + '" title="部署" onclick="intgDeploy(this)"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span></a>&nbsp;';
    return str;
}

function appendRunonceLink(str,integration_point_name,integration_point_version){
    var runoncehref = "/timer/intg/timer_run_trigger?task_type=Timer&task_name=" + integration_point_name + "_" + integration_point_version;
    str += '<a href="#" link="' + runoncehref + '" title="临时调度" onclick="runTrigger(this)"><span class="glyphicon glyphicon-repeat" aria-hidden="true"></span></a>&nbsp;';
    return str;
}

function appendEditLink(str,integration_point_name,integration_point_version){
    var edithref = "/timer/intg/edit?integration_point_name=" + integration_point_name
                    + "&integration_point_version=" + integration_point_version;
    str += '<a href="' + edithref + '" title="编辑集成点"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a>&nbsp;';
    return str;
}

function appendDelLink(str,integration_point_name,integration_point_version){
    var delhref = "/timer/intg/del?integration_point_name=" + integration_point_name
                    + "&integration_point_version=" + integration_point_version;
    str += '<a href="#" link=' + delhref + ' title="删除集成点" onclick="intgDel(this)"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></a>&nbsp;';
    return str;
}

// 临时调度接口
function runTrigger(node){
    var href = $(node).attr('link');
    $.ajax({
        type:"GET",
        async: false,
        url: href,
        data:{},
        datatype: "jsonp",
        success:function(data){
            if(data.status == 'SUCCESS'){
                // 表格刷新
                $('#intg_list_table').bootstrapTable('refresh');
            }else{
                alert('临时调度失败:' + data.result);
            }
        },
    });
}

function intgStart(node){
    var href = $(node).attr('link');
    $.ajax({
        type:"GET",
        async: false,
        url: href,
        data:{},
        datatype: "jsonp",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == 'SUCCESS'){
                // 页面刷新
                window.location.reload();
            }else{
                alert('启用:' + obj.result);
            }
        },
    });
}

function intgStop(node){
    var href = $(node).attr('link');
    $.ajax({
        type:"GET",
        async: false,
        url: href,
        data:{},
        datatype: "jsonp",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == 'SUCCESS'){
                // 页面刷新
                window.location.reload();
            }else{
                alert('停用失败:' + obj.result);
            }
        },
    });
}

function intgDeploy(node){
    var href = $(node).attr('link');
    $.ajax({
        type:"GET",
        async: false,
        url: href,
        data:{},
        datatype: "jsonp",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == 'SUCCESS'){
                // 页面刷新
                window.location.reload();
            }else{
                alert('部署失败:' + obj.result);
            }
        },
    });
}

function intgDel(node){
    var href = $(node).attr('link');
    $.ajax({
        type:"GET",
        async: false,
        url: href,
        data:{},
        datatype: "jsonp",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == 'SUCCESS'){
                // 页面刷新
                window.location.reload();
            }else{
                alert('删除失败:' + obj.result);
            }
        },
    });
}

function statusFormatter(value, row, index) {
    if(value == 0){
        return '<font color="#CC00FF">草稿</font>';
    }else if(value == 1){
        return '<font color="#3300FF">待部署</font>';
    }else if(value == 2){
        return '<font color="#FFCC00">启用</font>';
    }else if(value == 3){
        return '<font color="#0000CC">停用</font>';
    }else{
        return '<font color="#FF0000">未知</font>';
    }
}

function runLogFormatter(value, row, index) {
    if(value == 'NONE'){
        return '<font color="#888888">无运行状态</font>';
    }else if(value == 'SUCCESS'){
        return '<font color="#009900">' + value + '</font>';
    }else{
        return '<font color="#FF0000">' + value + '</font>';
    }
}

