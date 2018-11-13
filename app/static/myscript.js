//search dropdown button

dropdown_options = {
    hover: true
};

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, dropdown_options);
});

// $('.dropdown-trigger').dropdown();
