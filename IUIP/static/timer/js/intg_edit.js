var current_step = 1;   // 默认为第一步

$(function(){

    changeStepShow(current_step);

    // 下拉列表框渲染
    $('select').searchableSelect();

    $(".searchable-select-item").bind("click",function(){
        // 获取资源组名称
        var db_resource_name = $(this).parent().parent().parent().parent().parent().children('select').attr('value');
        if(db_resource_name != undefined && db_resource_name != "" && db_resource_name != null){        // value属性有值时表示表单回显
            var resource_name = $(this).parent().parent().parent().siblings(".searchable-select-holder").html(db_resource_name);
        }

        var resource_name = $(this).parent().parent().parent().siblings(".searchable-select-holder").html();

        // 获取对应的内容显示区
        var resourceInfoNode = $(this).parents(".resource_content").children(".resource_info");
        var connectionTestNode = $(this).parents(".resource_content").children(".connection_test");
        var name = $(this).parent().parent().parent().parent().siblings("select").attr("name");
        if(name == "src_resource"){
            $(document).data("src_resource_name",resource_name);
        }else if(name == "target_resource"){
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
                    $(resourceInfoNode).html(data.resource.resource_url);
                    $(resourceInfoNode).show();
                    // 连接测试
                    connectionTest(data.resource.resource_type,data.resource.resource_url,
                        data.resource.resource_username,data.resource.resource_password,resourceInfoNode,connectionTestNode);

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

function bindButtonEvent(){
    $(".build").click(function(){
        buildFieldMapping();
    });

    $(".save").click(function(){
        saveIntgConfig();
    });

    $(".next_step").click(function(){
        if(current_step < 3){
            current_step = current_step + 1;
            changeStepShow(current_step);
        }
    });

    $(".pres_step").click(function(){
        if(current_step > 1){
            current_step = current_step - 1;
            changeStepShow(current_step);
        }
    });
}

function changeStepShow(step){
    if(step == 1){
        // 隐藏进度条
        $(".first").show();
        $(".second").hide();
        $(".third").hide();
        // 隐藏内容区
        $("#intg_edit_resource").show();
        $("#sql_input").hide();
        $("#field_show").hide();
        // 按钮隐藏
        $(".pres_step").hide();
        $(".next_step").show();
        $(".build").hide();
        $(".save").hide();
    }else if(step == 2){
        // 隐藏进度条
        $(".first").show();
        $(".second").show();
        $(".third").hide();
        // 隐藏内容区
        $("#intg_edit_resource").hide();
        $("#sql_input").show();
        $("#field_show").hide();
        // 按钮隐藏
        $(".pres_step").show();
        $(".next_step").show();
        $(".build").hide();
        $(".save").hide();
    }else if(step == 3){
        // 隐藏进度条
        $(".first").show();
        $(".second").show();
        $(".third").show();
        // 隐藏内容区
        $("#intg_edit_resource").hide();
        $("#sql_input").hide();
        $("#field_show").show();
        // 按钮隐藏
        $(".pres_step").show();
        $(".next_step").hide();
        $(".build").show();
        $(".save").show();
    }
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

    $("#sql_data tbody tr:not(:first)").each(function(index, trNode){
        // 获取sql信息
        var src_sql = $(trNode).children("td:eq(1)").children("textarea").val();
        var target_sql = $(trNode).children("td:eq(2)").children("textarea").val();

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

function connectionTest(resource_type,resource_url,resource_username,resource_password,resourceInfoNode,connectionTestNode){
    $.ajax({
        type:"POST",
        async: false,
        url:"/resources/connectionTest/",
        data:{"dbType":resource_type,"url":resource_url,
            "username":resource_username,"password":resource_password},
        datatype: "jsonp",
        success:function(data){
            if(data.status == 'SUCCESS'){
                $(connectionTestNode).show();
                $(connectionTestNode).css('color', 'green');
                $(connectionTestNode).html("连接成功");

                $(connectionTestNode).siblings(".operate_more").show();
            }else{
                // 显示异常信息
                $(connectionTestNode).show();
                $(connectionTestNode).css('color', 'red');
                $(connectionTestNode).html(data.result);
            }
        },
    });
}

function sql_vlidate_all(node){
    $(node).parents("tbody").children("tr:not(:first)").each(function(index, trNode){
        // 获取资源组名称
        var src_resource_name = $(document).data("src_resource_name");
        var target_resource_name = $(document).data("target_resource_name");

        // 资源组详细信息
        var src_resource_data = $(document).data("resourceName_" + src_resource_name);
        var target_resource_data = $(document).data("resourceName_" + target_resource_name);

        // 获取sql信息
        var source_sql = $(trNode).children("td:eq(1)").children("textarea").val();
        var target_sql = $(trNode).children("td:eq(2)").children("textarea").val();

        // 清空提示信息信息
        $(trNode).children("td:last").html("");

        if(isCRSql(source_sql)){
            // sql验证
            validateSql(src_resource_data.resource_type,src_resource_data.resource_url,
                src_resource_data.resource_username,src_resource_data.resource_password,source_sql,trNode);
        }
        if(isCRSql(target_sql)){
            // sql验证
            validateSql(target_resource_data.resource_type,target_resource_data.resource_url,
                target_resource_data.resource_username,target_resource_data.resource_password,target_sql,trNode);
        }
    });
}

function sql_delete(node){
    if($(node).parents("tbody").children("tr").length > 2){
        $(node).parents("tr").remove();
    }
}

function sql_add(node){
    // 复制一行
    var row = $("#sql_data tbody").children("tr:eq(1)").clone();
    // 加到最后
    $(node).parents("tbody").append(row);
    // 清空元素
    $("#sql_data tbody").children("tr:last").children("td").children("textarea").text("");
    $("#sql_data tbody").children("tr:last").children("td:last").html("");
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
            // 获取提示信息
            var msg = $(tr).children("td:last").html();
            if(data.status == "SUCCESS"){
                msg = msg + "<font size='3px;' style='color:green;'>验证成功!</font><br>";
            }else{
                msg = msg + "<font size='2px;' style='color:red;'>验证失败!" + data.result + "</font><br>";
            }
            $(tr).children("td:last").html(msg);
        },
    });
}

// 判断是否 CR 开头
function isCRSql(sql){
    var index1 = sql.trim().toUpperCase().indexOf("SELECT ");
    var index2 = sql.trim().toUpperCase().indexOf("INSERT ");
    if(index1 == 0 || index2 == 0){
        return true;
    }
    return false;
}

// 判断是否 UD 开头
function isUDSql(sql){
    var index1 = sql.trim().toUpperCase().indexOf("UPDATE ");
    var index2 = sql.trim().toUpperCase().indexOf("DELETE ");
    if(index1 == 0 || index2 == 0){
        return true;
    }
    return false;
}