$(document).ready(function(){
    $.ajax({
        url:'/showevaluation',
        dataType: "json",
        type:'GET'
        })
        // Ajaxリクエストが成功した時発動
        .done(function(data){
            result = data.data
            row_count = result.length
            console.log(result)
            for(var i = 0; i < row_count; i++){
                console.log(result[i])
                columns_count = result[i].length
                console.log(columns_count)
                add_html =""
                for(var j = 0;j<columns_count;j++){
                    if(i==0){
                        add_html = add_html + "<th>" + result[i][j] + "</th>"
                    }else{
                        add_html = add_html + "<td>" + result[i][j] + "</td>"
                    }
                }
                $('.evaluation_table').append("<tr>" + add_html + "</tr>");
                add_html = ""
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