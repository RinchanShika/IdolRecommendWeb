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
                img_html = "<img src='../static/img/" + like_list[i] + "/" + like_list[i] + " (1).jpg'>";
                $('.like_list').append(put_html);
                $('.like_list').append(img_html);
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