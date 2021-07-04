// (function($){
//     $(function(){
      
//       $('.sidenav').sidenav();
//       $('.tabs').tabs();
//       $('.materialboxed').materialbox();
//       $('select').formSelect();
//       $('.slider').slider();
//       $('.tooltipped').tooltip();
//       $('.modal').modal();

//     }); // end of document ready
// })(jQuery); // end of jQuery name space

$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.tabs').tabs();
    $('.materialboxed').materialbox();
    $('select').formSelect();
    $('.slider').slider();
    $('.tooltipped').tooltip();
    $('.modal').modal();
    $('.collapsible').collapsible();
    $('.datepicker').datepicker({format:'yyyy-mm-dd'});
})