$(document).ready(function(){
    $.ajax({
        url:'/displayaddlist',
        dataType: "json",
        type:'GET'
        })
        // Ajaxリクエストが成功した時発動
        .done(function(data){
            add_list = data.data;
            if(add_list.length == 0){
                 $('.add_list').append("承認待ちはありません");
            }
            for (var i = 0 ; i < add_list.length;i++){
                member = add_list[i]
                put_html =
                   "<p><table border='1'>" +
                   "<tr><th>名前</th><td>"+ member[1] + "</td></tr>" +
                   "<tr><th>グループ名</th><td>"+ member[2] + "</td></tr>" +
                   "<tr><th>TwitterID</th><td>"+ member[3] + "</td></tr>" +
                   "<tr><th>InstagramID</th><td>"+ member[4] + "</td></tr>" +
                   "<tr><th></th><td><img id='thumbnail' src='../static/etcimg/" + member[5] + "'</td></tr>" +
                   "</table>" +
                   "<button type='button' onclick='location.href=" + '"/aprovalAddIdol/' + member[0] + '"' + "'>承認</button>　" +
                   "<button type='button' onclick='location.href=" + '"/disaprovalAddIdol/' + member[0] + '"' + "'>削除</button></p></p>"
                $('.add_list').append(put_html);
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
