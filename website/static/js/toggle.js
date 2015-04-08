var utils = require('./utils')


function Toggle(element) {
    this.element = element;
    this.contentSelector = element.getAttribute('data-toggle');
    this.attach();
}


Toggle.prototype = {
    attach: function() {
        this.element.addEventListener('click', this.toggle.bind(this));
        document.addEventListener('click', this.documentClicked.bind(this));
    },

    elementClicked: function(event) {
        this.toggle();
    },

    documentClicked: function(event) {
        var target = event.target;
        if (utils.isWithin(target, this.element)){
            return;
        }

        var content_list = this.getContentElements();
        for (var i = 0, el; el = content_list[i++];) {
            if (utils.isWithin(target, el)) {
                return;
            }
        }

        this.hide();
    },

    toggle: function() {
        this.forEachContentElement(function(el) {
            utils.toggleAttribute(el, 'hidden');
        });
    },

    show: function() {
        this.forEachContentElement(function(el) {
            el.removeAttribute('hidden');
        });
    },

    hide: function() {
        this.forEachContentElement(function(el) {
            el.setAttribute('hidden', '');
        });
    },

    forEachContentElement: function(f) {
        var content_list = this.getContentElements();
        for (var i = 0, el; el = content_list[i++];) {
            f(el);
        }
    },

    getContentElements: function() {
        return document.querySelectorAll(this.contentSelector);
    }
}


module.exports = Toggle;
