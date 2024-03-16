document.getElementById('urlForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const urlInput = document.getElementById('urlInput').value;
    const urlType = document.getElementById('urlType').value;
    const limit = document.getElementById('limit').value;
    const model = document.getElementById('modelType').value;

    if(urlType === "ptt"){
        alert('submit success')
        fetch('/craw?url=' + encodeURIComponent(urlInput) + '&limit=' + limit + '&model=' + model)
        .then(response => response.text())
        .then(result => {
            const Rs = JSON.parse(result);
            document.getElementById('result').textContent = Rs[0];
            document.getElementById('result1').textContent = Rs[1];
            document.getElementById('prate').textContent = Rs[2];
            document.getElementById('neurate').textContent = Rs[3];
            document.getElementById('negrate').textContent = Rs[4];
            document.getElementById('len').textContent = Rs[5];
            document.getElementById('info').innerHTML = Rs[6];
            document.getElementById('zz').innerHTML = Rs[7];
        })
        .catch(error => {
            console.error('error:', error);
        });
    }
});
function get(x) {
    return document.location.search.split(x + '=')[1] ? (document.location.search.split(x + '=')[1].split('&')[0]) : '';
}
var timer,autolen;
window.onload = function() {
    timer = setInterval(function() {
        fetch('/progress')
        .then(response => response.text())
        .then(result => {
            const Rs = JSON.parse(result);
            document.getElementById('progress').innerHTML = Rs[0] + '&percnt;';
            document.getElementsByClassName('progressbar').innerHTML = '<div class="determinate" style="width: ' + Rs[0] + '%"></div>'
            document.getElementById('info').innerHTML = Rs[1];
        })
        .catch(error => {
            console.error('error:', error);
        });
    },100);
    document.getElementById('urlInput').value = get('pre');
    getlen();
}
function getlen() {
    document.getElementById('len_post').innerHTML = '...';
    fetch('/get_len?url=' + document.getElementById('urlInput').value)
    .then(response => response.text())
    .then(result => {
        const Rs = JSON.parse(result);
        if(Rs == ' ') document.getElementById('len_post').innerHTML = '';
        else document.getElementById('len_post').innerHTML = Rs;
    })
    .catch(error => {
        console.error('error:', error);
    });
}