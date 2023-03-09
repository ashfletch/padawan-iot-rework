const lightSchemeIcon = document.querySelector('link#icon-light-scheme');
const darkSchemeIcon = document.querySelector('link#icon-dark-scheme');

function onUpdate() {
    if (matcher.matches) {
        lightSchemeIcon.remove();
        document.head.append(darkSchemeIcon);
    } else {
        document.head.append(lightSchemeIcon);
        darkSchemeIcon.remove();
    }
}

const matcher = window.matchMedia('(prefers-color-scheme: dark)');
onUpdate();