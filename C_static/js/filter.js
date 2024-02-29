$(document).ready(function() {
    $(".filter-button").click(function() {
      var value = $(this).attr('data-filter');
      if (value == "all") {
        $(".filter").show('1000');
      } else {
        $(".filter").hide();
        $('.category-' + value).parent().show('1000');
      }
    });
  });