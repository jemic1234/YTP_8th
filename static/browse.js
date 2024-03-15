// document.getElementById('urlForm').addEventListener('submit', function(event) {
//     event.preventDefault();

//     const urlInput = document.getElementById('urlInput').value;
//     const urlType = document.getElementById('urlType').value;
//     const limit = document.getElementById('limit').value;
//     const model = document.getElementById('modelType').value;

//     if(urlType === "ptt"){
//         alert('submit success')
//         fetch('/craw?url=' + encodeURIComponent(urlInput) + '&limit=' + limit + '&model=' + model)
//         .then(response => response.text())
//         .then(result => {
//             const Rs = JSON.parse(result);
//             document.getElementById('result').textContent = Rs[0];
//             document.getElementById('result1').textContent = Rs[1];
//             document.getElementById('prate').textContent = Rs[2];
//             document.getElementById('neurate').textContent = Rs[3];
//             document.getElementById('negrate').textContent = Rs[4];
//             document.getElementById('len').textContent = Rs[5];
//             document.getElementById('info').innerHTML = Rs[6];
//         })
//         .catch(error => {
//             console.error('error:', error);
//         });
//     }
// });

function get(x) {
    return document.location.search.split(x + '=')[1] ? (document.location.search.split(x + '=')[1].split('&')[0]) : '';
}

window.onload = function() {
    // alert('1');
    var s = ''
    s = (get('board'));
    // alert('/ptt_board?board=' + s);
    fetch('/ptt_board?board=' + s)
        .then(response => response.text())
        .then(result => {
            // alert(result);
            // const Rs = JSON.parse(result);
            if(result === 'analysis') location.href = '/?pre=https://www.ptt.cc' + s;
            document.getElementById('info').innerHTML = result;
        })
        .catch(error => {
            console.error('error:', error);
        });
};