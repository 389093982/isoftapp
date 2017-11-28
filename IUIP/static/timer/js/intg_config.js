$(function(){
    // 下拉列表框渲染
    $('select').searchableSelect();

    $('#btn_reset').click(function(){
        $('#intg_config')[0].reset();
    });
});
