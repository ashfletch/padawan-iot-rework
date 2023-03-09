const year = Number(new Date().getFullYear());
document.currentScript.insertAdjacentHTML(
    'beforebegin',
    (year > 2020 ? `${year}` : '')
)