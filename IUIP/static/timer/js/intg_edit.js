$(function(){

    // 下拉列表框渲染
    $('select').searchableSelect();

    $(".searchable-select-item").bind("click",function(){
        // 获取资源组名称
        var db_resource_name = $(this).parent().parent().parent().parent().parent().children('select').attr('value');
        if(db_resource_name != undefined && db_resource_name != "" && db_resource_name != null){        // value属性有值时表示表单回显
            var resource_name = $(this).parent().parent().parent().siblings(".searchable-select-holder").html(db_resource_name);
        }

        var resource_name = $(this).parent().parent().parent().siblings(".searchable-select-holder").html();

        // 获取对应的 textarea
        var resourceNode;
        var msgNode;
        var name = $(this).parent().parent().parent().parent().siblings("select").attr("name");
        if(name == "src_resource"){
            resourceNode = $("textarea[class='src_resource']");
            msgNode = $(".srcMsg");

            $(document).data("src_resource_name",resource_name);
        }else if(name == "target_resource"){
            resourceNode = $("textarea[class='target_resource']");
            msgNode = $(".destMsg");

            $(document).data("target_resource_name",resource_name);
        }

        // 获取资源组信息
        $.ajax({
            url: "/resources/queryResourceByName/",
            type:"POST",
            data: {"resourceName":resource_name},
            success: function(data){
                if(data.status == "success"){
                    // 设置文本域内容为 url
                    $(resourceNode).val(data.resource.resource_url);
                    // 连接测试
                    connectionTest(data.resource.resource_type,data.resource.resource_url,
                        data.resource.resource_username,data.resource.resource_password,resourceNode,msgNode);

                    // 缓存资源组信息
                    $(document).data("resourceName_" + data.resource.resource_name, data.resource);
                }else{
                    $(msgNode).show();
                    $(msgNode).css('color', 'red');
                    $(msgNode).html("资源组加载异常!");
                }
            }
        });
    });

    bindEvent();
})

function bindEvent(){
    bindButtonEvent();
    bindHrefEvent();
    bindInitEvent();
}

function bindInitEvent(){
    var src_resource = $("select[name='src_resource']").attr("value");
    var target_resource = $("select[name='target_resource']").attr("value");
    if(src_resource != undefined && src_resource != "" && src_resource != null &&
        target_resource != undefined && target_resource != "" && target_resource != null){
        $(".searchable-select-item").trigger("click");
    }
}

function bindHrefEvent(){

    $(".sql_view").click(function(){
        var tr = $(this).parent().parent();
        var source_sql = $(tr).children("td:eq(0)").html();
        var target_sql = $(tr).children("td:eq(1)").html();

        $("#sql_source_input").val(source_sql);
        $("#sql_target_input").val(target_sql);
        $(document).data("modifyTr",tr);
    });

    $(".sql_delete").click(function(){
        $(this).parent().parent().remove();
    });

    $(".sql_vlidate").click(function(){
        var validating = $(this).data("validating");
        // 验证中的不能再验证
        if(validating != true){
             $(this).data("validating",true);

            // 获取资源组名称
            var src_resource_name = $(document).data("src_resource_name");
            var target_resource_name = $(document).data("target_resource_name");
            // 资源组详细信息
            var src_resource_data = $(document).data("resourceName_" + src_resource_name);
            var target_resource_data = $(document).data("resourceName_" + target_resource_name);

            // 获取sql信息
            var tr = $(this).parent().parent();
            var source_sql = $(tr).children("td:eq(0)").html();
            var target_sql = $(tr).children("td:eq(1)").html();

            $(tr).children("td:last").children(".wait_validate").hide();
            $(tr).children("td:last").children(".validating").show();
            $(tr).children("td:last").children(".msg").text("");

            // sql验证
            validateSql(src_resource_data.resource_type,src_resource_data.resource_url,
                src_resource_data.resource_username,src_resource_data.resource_password,source_sql,tr);
            validateSql(target_resource_data.resource_type,target_resource_data.resource_url,
                target_resource_data.resource_username,target_resource_data.resource_password,target_sql,tr);

            $(tr).children("td:last").children(".wait_validate").hide();
            $(tr).children("td:last").children(".validating").hide();

            $(this).data("validating",false);
        }
    });
}

function validateSql(resource_type,resource_url,resource_username,resource_password,sql,tr){
    $.ajax({
        type:"POST",
        async: false,
        url:"/timer/validateSql/",
        data:{"resource_type":resource_type, "resource_url":resource_url,
            "resource_username":resource_username, "resource_password":resource_password, "sql":sql},
        datatype: "jsonp",
        success:function(data){
            if(data.status == "SUCCESS"){
                var msg = "<p style='color:green;'>验证成功!</p>";
            }else{
                var msg = "<p style='color:red;'>验证失败!" + data.result + "</p>";
            }
            var html = $(tr).children("td:last").children(".msg").html();
            $(tr).children("td:last").children(".msg").html(html + msg);
        },
    });
}

function bindButtonEvent(){
    $("#sql_add").click(function(){
        var source_sql = $("#sql_source_input").val();
        var target_sql = $("#sql_target_input").val();

        if(!isStantardSql(source_sql) || !isStantardSql(target_sql)){
            $(".sql_format_error").show();
            return;
        }else{
            $(".sql_format_error").hide();
        }

        if($(document).data("modifyTr") != null && $(document).data("modifyTr") != undefined){
            // 修改模式
            var tr = $(document).data("modifyTr");
            $(tr).children("td:eq(0)").html(source_sql);
            $(tr).children("td:eq(1)").html(target_sql);
            $(document).removeData("modifyTr");
        }else{
            // 新增模式
            var operate = "<a href=\"#\" class=\"sql_view\" title=\"编辑\"><span class=\"glyphicon glyphicon-pencil\" aria-hidden=\"true\"></span></a>"
                                + "<a href=\"#\" class=\"sql_delete\" title=\"删除\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a>"
                                + "<a href=\"#\" class=\"sql_vlidate\" title=\"验证\"><span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span></a>";

            var label = "<span class='wait_validate'>待验证</span>"
                + "<span><img class='validating' src='/static/common/img/Loading2.gif' style='width:20px;height:20px;display: none;'></span>"
                + "<span class='msg'></span><br>";
            var tr = "<tr class=\"warning\"><td>" + source_sql + "</td><td>" + target_sql + "</td><td>" + operate + "</td><td>" + label + "</td></tr>";
            $("#sql_data").append(tr);
            // 重新绑定事件
            bindHrefEvent();
        }

    });

    $("#sql_reset").click(function(){
        $("#sql_source_input").val("");
        $("#sql_target_input").val("");
    });
    
    $("#batch_validate").click(function(){
        $(".sql_vlidate").each(function(){
            $(this).trigger("click");
        });
    });

    $("#build").click(function(){
        buildFieldMapping();
    });

    $("#saveIntgConfig").click(function(){
        saveIntgConfig();
    });
}

function saveIntgConfig(){
    var source_client_name = $("#source_client_name").html();
    var target_client_name = $("#target_client_name").html();

    var integration_point_name = $("#integration_point_name").html();
    var integration_point_version = $("#integration_point_version").html();
    // 获取资源组名称
    var src_resource_name = $(document).data("src_resource_name");
    var target_resource_name = $(document).data("target_resource_name");

    var sqlArray = $(document).data("sqlArray");
    var fieldMappingArray = $(document).data("fieldMappingArray");

    $.ajax({
        type:"POST",
        async: false,
        url:"/timer/saveIntgConfig/",
        data:{
            "source_client_name":source_client_name,
            "target_client_name":target_client_name,
            "integration_point_name":integration_point_name,
            "integration_point_version":integration_point_version,
            "src_resource_name":src_resource_name,
            "target_resource_name":target_resource_name,
            "sqlArray":JSON.stringify(sqlArray),
            "fieldMappingArray":JSON.stringify(fieldMappingArray)
        },
        datatype: "jsonp",
        success:function(data){
            var obj = JSON.parse(data);
            if(obj.status == 'SUCCESS'){
                window.location.href='/timer/intg/list/';
            }else{
                alert(obj.result);
            }
        }
    });
}

function buildFieldMapping(){
    // 置空 UI
    $(".fieldMappingAccordion").html("");

    var sqlArray = new Array();
    var fieldMappingArray = new Array();

    $("#sql_data tr:not(:first)").each(function(index){
        var src_sql = $(this).children("td:eq(0)").html();
        var target_sql = $(this).children("td:eq(1)").html();

        var array = new Array();
        array.push(src_sql);
        array.push(target_sql);
        sqlArray.push(array);
        $(document).data("sqlArray",sqlArray);

        // 获取资源组名称
        var src_resource_name = $(document).data("src_resource_name");
        var target_resource_name = $(document).data("target_resource_name");
        // 资源组详细信息
        var src_resource_data = $(document).data("resourceName_" + src_resource_name);
        var target_resource_data = $(document).data("resourceName_" + target_resource_name);

        $.ajax({
            type:"POST",
            async: false,
            url:"/timer/getMetaData/",
            data:{
                "src_sql":src_sql,
                "src_resource_type":src_resource_data.resource_type,
                "src_resource_url":src_resource_data.resource_url,
                "src_resource_username":src_resource_data.resource_username,
                "src_resource_password":src_resource_data.resource_password,
                "target_sql":target_sql,
                "target_resource_type":target_resource_data.resource_type,
                "target_resource_url":target_resource_data.resource_url,
                "target_resource_username":target_resource_data.resource_username,
                "target_resource_password":target_resource_data.resource_password
            },
            datatype: "jsonp",
            success:function(data){
                if(data.status = 'SUCCESS'){
                    renderFieldMappingUI(data,index);

                    // 缓存字段 mapping 信息
                    var src_meta = data.src_meta;
                    var target_meta = data.target_meta;
                    if(src_meta.status == 'SUCCESS' && target_meta.status == 'SUCCESS'){
                        var src_meta_data = src_meta.result;
                        var target_meta_data = target_meta.result;

                        var array = new Array()
                        array.push(src_meta_data)
                        array.push(target_meta_data)
                        fieldMappingArray.push(array);

                        $(document).data("fieldMappingArray",fieldMappingArray);
                    }
                }else{
                    alert(data.result);
                }
            }
        });
    });
}

function renderFieldMappingUI(data,index){
    // index 从 1 开始计数
    index ++;
    var src_meta = data.src_meta;
    var target_meta = data.target_meta;
    if(src_meta.status == 'SUCCESS' && target_meta.status == 'SUCCESS'){
        var src_meta_data = src_meta.result;
        var target_meta_data = target_meta.result;

        var maxRow = 0;
        if(src_meta_data.length > target_meta_data.length){
            maxRow = src_meta_data.length;
        }else{
            maxRow = target_meta_data.length;
        }

        var rows = "";
        for(var i=0; i<maxRow; i++){
            var src_td = "";
            if(i < src_meta_data.length){
                // 有值
                src_td = "<td>" + src_meta_data[i][0] + "</td>";
            }else{
                // 无值
                src_td = "<td></td>";
            }
            var target_td = "";
            if(i < target_meta_data.length){
                target_td = "<td>" + target_meta_data[i][0] + "</td>";
            }else{
                target_td = "<td></td>";
            }

            var color = i % 2 == 0 ? "warning" : "success";
            rows += "<tr class='" + color + "'>" + src_td + target_td + "</tr>";
        }

        var html = "<div class=\"am-panel am-panel-success\"><div class=\"am-panel-hd\">"
                + "<h4 class=\"am-panel-title\" data-am-collapse=\"{parent: '#accordion1', target: '#fieldMapping_" + index + "'}\">第 " + index + " 组字段 mapping</h4>"
            + "</div>"
            + "<div id=\"fieldMapping_" + index + "\" class=\"am-panel-collapse am-collapse\">"
                + "<table class=\"table table-bordered\">"
                    + "<tr class=\"info\"><td>字段名称</td><td>字段名称</td></tr>"
                    + rows
                + "</table>"
            + "</div></div>";
        $(".fieldMappingAccordion").append(html);
    }else{
        alert(src_meta.status);
        alert(target_meta.status);
    }
}

function isStantardSql(sql){
    // 可以为空
    if(isNull(sql)){
        return true;
    }
    // 判断是否 CRUD 开头
    var index1 = sql.trim().toUpperCase().indexOf("SELECT ");
    var index2 = sql.trim().toUpperCase().indexOf("INSERT ");
    var index3 = sql.trim().toUpperCase().indexOf("UPDATE ");
    var index4 = sql.trim().toUpperCase().indexOf("DELETE ");
    if(index1 == 0 || index2 == 0 || index3 == 0 || index4 == 0){
        return true;
    }
    return false;
}

// 判断字符串是否为空
function isNull(str){
    if(str == "")
        return true;
    var regu = "^[ ]+$";
    var re = new RegExp(regu);
    return re.test(str);
}

function connectionTest(resource_type,resource_url,resource_username,resource_password,resourceNode,msgNode){
    $.ajax({
        type:"POST",
        async: false,
        url:"/resources/connectionTest/",
        data:{"dbType":resource_type,"url":resource_url,
            "username":resource_username,"password":resource_password},
        datatype: "jsonp",
        success:function(data){
            if(data.status == 'SUCCESS'){
                $(msgNode).show();
                $(msgNode).css('color', 'green');
                $(msgNode).html("连接成功");
            }else{
                // 显示异常信息
                $(msgNode).show();
                $(msgNode).css('color', 'red');
                $(msgNode).html(data.result);
            }
        },
    });
}
