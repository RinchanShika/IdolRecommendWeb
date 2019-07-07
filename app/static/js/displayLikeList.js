$(document).ready(function(){
    $.ajax({
        url:'/displaylikelist',
        dataType: "json",
        type:'GET'
        })
        // Ajaxリクエストが成功した時発動
        .done(function(data){
            like_list = data.data.like_list;
            like_list_twitter = data.data.like_list_twitter;
            for (var i = 0 ; i < like_list.length;i++){
                put_html = like_list[i] + '';
                $('.like_list').append(put_html);
                if(like_list_twitter[i] != ''){
                    twitter_html = "  <a href = 'https://twitter.com/" + like_list_twitter[i] + "' target='_blank'>Twitter</a>";
                    $('.like_list').append(twitter_html);
                }
                img_html = "</br><img class='likelist_image' src='../static/img/" + like_list[i] + "/" + like_list[i] + " (1).jpg'><br></br>";
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
