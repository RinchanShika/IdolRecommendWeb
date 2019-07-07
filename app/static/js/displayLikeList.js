$(document).ready(function(){
    $.ajax({
        url:'/displaylikelist',
        dataType: "json",
        type:'GET'
        })
        // Ajaxリクエストが成功した時発動
        .done(function(data){
            like_list = data.data.like_list;
            console.log(like_list)
            for (var i = 0 ; i < like_list.length;i++){
                put_html = like_list[i] + '</br>';
                $('.like_list').append(put_html);
            }
        })
        // Ajaxリクエストが失敗した時発動
        .fail( (data) => {
            alert(data);
            console.log(data);
        })
        // Ajaxリクエストが成功・失敗どちらでも発動
        .always( (data) => {
        });
});