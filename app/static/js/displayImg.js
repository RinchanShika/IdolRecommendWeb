$(document).ready(function(){
    alert('呼ばれたよ～')

    $.ajax({
        url:'http://l27.0.0.1:5000/getFirstList',
        dataType: "json"
        type:'GET',
        data:{
        }
        })
        // Ajaxリクエストが成功した時発動
        .done( (data) => {
            alert(data);
            for( var = i; i < data[0].length; i++){
                put_html = '<div class="avatar"  style="display: block; background-image: url(' + data[1][i] + ')"></div>';
                $('.buddy').eq(i).html(data);
            }
            console.log(data);
        })
        // Ajaxリクエストが失敗した時発動
        .fail( (data) => {
            alert(data);
            console.log(data);
        })
        // Ajaxリクエストが成功・失敗どちらでも発動
        .always( (data) => {

        });


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
});