var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    //document.querySelector('#nav').style.boxShadow = 'none';
    $('#nav').fadeIn('slow');
    $('#nav').css('box-shadow','0px 0px 5px black')
  } else {
    //document.querySelector('#nav').style.boxShadow = '0px 0px 5px black';
    $('#nav').fadeIn('slow');
    $('#nav').css('box-shadow','0px 0px 5px black')
  }
  prevScrollpos = currentScrollPos;
}
