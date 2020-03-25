function request_get(func, url) {
    let xhr = new XMLHttpRequest();
    xhr.onloadend = func;
    xhr.open('get',host + url,true);
    xhr.send();
}