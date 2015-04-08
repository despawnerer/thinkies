module.exports = {
    isWithin: function(child, parent) {
        if (child == parent) {
            return true;
        } else if (!child.parentNode) {
            return false;
        } else {
            return this.isWithin(child.parentNode, parent);
        }
    },

    toggleAttribute: function(el, attr, value) {
        if (el.hasAttribute(attr)) {
            el.removeAttribute(attr);
        } else {
            el.setAttribute(attr, value);
        }
    }
}
