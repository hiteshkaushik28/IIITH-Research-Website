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
sidenav_options = {};

document.addEventListener('DOMContentLoaded', function()
{
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, sidenav_options);
});