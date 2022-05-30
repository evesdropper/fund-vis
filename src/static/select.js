// ty stackoverflow 
$(function() {    // Makes sure the code contained doesn't run until
                  //     all the DOM elements have loaded

    $('#modelselector').change(function(){
        $('.models').hide();
        $('#' + $(this).val()).show();
    });

});