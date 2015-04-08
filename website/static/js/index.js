var Toggle = require('./toggle');


var toggle_list = document.querySelectorAll('[data-toggle]');
for (var i = 0, el; el = toggle_list[i++];) {
    new Toggle(el);
}
