$(document).ready (function(){
    $(".nav a").on("click", function(){
                   $(".nav").find(".active").removeClass("active");
                   $(this).parent().addClass("active");
     });

     $(".alert").fadeTo(2000, 500).slideUp(500, function(){
        $("ul#flashed-alert").slideUp(500);
    });
});
