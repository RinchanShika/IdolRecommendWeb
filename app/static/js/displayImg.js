$(document).ready(function(){

    $(".buddy").on("swiperight",function(){
      $(this).addClass('rotate-left').delay(700).fadeOut(1);
      $('.buddy').find('.status').remove();

      $(this).append('<div class="status like">Like!</div>');
      if ( $(this).is(':last-child') ) {
        $('.buddy:nth-child(1)').removeClass ('rotate-left rotate-right').fadeIn(300);
       } else {
          $(this).next().removeClass('rotate-left rotate-right').fadeIn(400);
       }
    });

   $(".buddy").on("swipeleft",function(){
    $(this).addClass('rotate-right').delay(700).fadeOut(1);
    $('.buddy').find('.status').remove();
    $(this).append('<div class="status dislike">Dislike!</div>');

    if ( $(this).is(':last-child') ) {
     $('.buddy:nth-child(1)').removeClass ('rotate-left rotate-right').fadeIn(300);
      alert('OUPS');
     } else {
        $(this).next().removeClass('rotate-left rotate-right').fadeIn(400);
    }
  });

      $.ajax({
        url:'/getFirstList',
        dataType: "json",
        type:'GET'
        })
        // Ajaxリクエストが成功した時発動
        .done(function(data){
            name = data.data.name;
            image = data.data.image;
            imgUrl = "'../static/img/" + name + "/" + image + "'";
            put_html = '<div class="avatar"  style="display: block; background-image: url( ' + imgUrl + ')"></div>';
            $('.buddy').append(put_html);
            $('.member_name').append(name)
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

function putEvaluation(eval){
    $(function(){
        $.ajax({
        url:'/putEvaluation',
        dataType: "json",
        contentType: 'application/json',
        data: JSON.stringify({
            "name": $('.member_name').text(),
            "eval": eval
        }),
        type:'POST'
        })
        // Ajaxリクエストが成功した時発動
        .done(function(data){
            name = data.data.name;
            image = data.data.image;
            imgUrl = "'../static/img/" + name + "/" + image + "'";
            put_html = '<div class="avatar"  style="display: block; background-image: url( ' + imgUrl + ')"></div>';
            $('.buddy').html(put_html);
            $('.member_name').html(name)
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
}