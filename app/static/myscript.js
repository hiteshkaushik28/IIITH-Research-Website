//search dropdown button
dropdown_options = {
    hover: true,
    alignment: 'bottom',
    constrainWidth: false
};

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, dropdown_options);
});

//sidenav
document.addEventListener('DOMContentLoaded', function()
{
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {});
});

$(document).ready(function(e){

    // Search Box
    $('.search_row .dropdown-content').find('a').click(function(e) {
        e.preventDefault();
        var category = $(this).children()[1].innerHTML;
        $('#search_box').val("");
        $("#search_box").attr('disabled', false);
        $("#search_box").attr('placeholder', "Search " + category);
        $("#hidden_category").val(category);
    });
});