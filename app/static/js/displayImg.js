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
            name1 = data.data.name1;
            image1 = data.data.image1;
            imgUrl1 = "'../static/img/" + name1 + "/" + image1 + "'";
            put_html1 = '<div class="avatar"  style="display: block; background-image: url( ' + imgUrl1 + ')"></div>';
            $('.buddy').html(put_html1);
            $('.member_name').append(name1)

            name2 = data.data.name2;
            image2 = data.data.image2;
            imgUrl2 = "'../static/img/" + name2 + "/" + image2 + "'";
            put_html2 = '<div class="next_avatar"  style="background-image: url( ' + imgUrl2 + ')"></div>';
            $('.buddy').append(put_html2);
            $('.next_member_name').append(name2)
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
            //avatarを削除
            $('.avatar').remove();
            //member_nameを削除
            $('.member_name').remove();
            //next_avatarをavatarに
            $('.next_avatar').addClass('avatar').removeClass('next_avatar')
            //next_member_nameをmember_nameに
            $('.next_member_name').addClass('member_name').removeClass('next_member_name')

            //next_avatarを追加
            //next_member_nameを追加
            name = data.data.name;
            image = data.data.image;
            imgUrl = "'../static/img/" + name + "/" + image + "'";
            put_html = '<div class="next_avatar" style="background-image: url( ' + imgUrl + ')"></div>';
            name_html = '<span class="next_member_name">' + name + '</span>'
            $('.buddy').append(put_html);
            $('.member_name_area').append(name_html)
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