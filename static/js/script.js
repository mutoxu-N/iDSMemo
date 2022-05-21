
function memo_clicked(e) {
    memos = document.getElementsByClassName('memo');
    for(var i=memos.length-1; i>=0; i--){
        if(memos[i].onclick == null){
            if(memos[i] == this) memos[i].classList.add('active');
            else memos[i].classList.remove('active');
        }
    }
}

function add_memo(content) {
    var c = document.getElementById('container');
    var newElement = document.createElement('div');
    newElement.classList.add('memo');
    newElement.textContent = '・' + content;
    newElement.addEventListener("click", memo_clicked);
    c.appendChild(newElement);

}

// clicked
document.body.onclick = function(e) {
    console.log(e.clickX);
}

// memo create
for(var i=0; i<100; i++){
    add_memo(i+1)
}

