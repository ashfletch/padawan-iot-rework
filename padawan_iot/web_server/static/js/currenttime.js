const utctime = new Date().toISOString().substring(0,19);
document.currentScript.insertAdjacentHTML(
    'beforebegin',
    `${utctime.replace('T', ' ')} UTC`
)