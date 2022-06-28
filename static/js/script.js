const addr = "http://127.0.0.1:8080/";
const Type = {new: 1, edit:2, remove:3, check: 4};
const KeyNum = {enter: 13, up: 38, down: 40, left: 37, right: 39};
cursorPos = null
memoData = {}

function send(data) {
    $.ajax({
        url:addr + "receive",
        type:"POST", 
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'

    }).done(function(res, textStatus, jqXHR ){
        memoData = res;
        reload(data);

    }).fail(function(jqXHR, textStatus, errorThrown){
        console.log("failed");

    });
}

function set_focus(element, pos=0) {
    console.log(pos);
    setTimeout(() => element.focus(), 0);

    document.getSelection().removeAllRanges();
}
function get_memo_idx(element) { return $(element).index(); }
function add() {
    send({type: Type["new"], text: $(':focus').text()});        
    $("div#last").empty();
}
function edit() {
    send({type: Type["edit"], id: get_memo_idx($(':focus').parent().parent().parent()), text: $(':focus').text()});
}


function reload(data) {
    // remove all children
    $("#container > div.memo ").remove()

    // rebuild screen
    for(i=0; i<memoData.length; i++) {
        $('<div class="memo">\
                <ul style="margin-bottom: 0px;">\
                    <li><div class="content" contenteditable="true">'+ memoData[i] +'</div><button class="rm">削除</button></li>\
                </ul>\
            </div>'
        ).insertBefore('div#last')

    }

    // element settings
    $("div.content").keydown((e) => {
        // edit
        switch(e.keyCode) {
            case KeyNum["enter"]:
                edit();
                return false;

            case KeyNum["down"]:
                currentId = get_memo_idx($(':focus').parent().parent().parent());
                if(currentId+1 === memoData.length){
                    set_focus($('div#last'));
                } else {
                    len = memoData[currentId+1].length;
                    set_focus($('#container > div.memo:nth-child(' + (currentId+2) + ') > ul > li > div.content'), len);
                }
                break;

            case KeyNum["up"]:
                currentId = get_memo_idx($(':focus').parent().parent().parent());
                if (currentId > 0) {
                    len = memoData[currentId-1].length;
                    set_focus($('#container > div.memo:nth-child(' + (currentId) + ') > ul > li > div.content'), len);
                }
                break;

        }
    })
    $("button.rm").on("click", (e) => {
        send({type: Type["remove"], id: get_memo_idx($(e.currentTarget).parent().parent().parent())})
    })
    

    // focus
    switch(data.type){
        case Type["new"]:
            set_focus($('div#last'));
            break;
        case Type["edit"]:
            set_focus($('#container > div.memo:nth-child(' + (data.id+2) + ') > ul > li > div.content'));
            break;
    }

}



// element settings
$("div#last").keydown((e) => {
    // add
    if (e.keyCode === KeyNum["enter"]) {
        add();
        return false;
    } else if(e.keyCode === KeyNum["up"]) {
        set_focus($('#container > div.memo:nth-child(' + (memoData.length) + ') > ul > li > div.content'));
    }
});

// get data from flask and display
send({type: Type["check"]});

//TODO EDITフォーカスが外れたら変更内容をFlaskに送る
//TODO カーソルの位置を保存して、メモを移動したときにカーソルの位置を設定する。