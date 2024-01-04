$(function() {
  $love = $('.heart');
  for( var i = 0; i < 4; i++) {
    $('.wrapper').append($love.clone());
  }
});
