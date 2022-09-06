const addr = "http://127.0.0.1:8080/";
const Type = {new: 1, edit:2, remove:3, check: 4, f_open:5, f_new: 6, undo:7, redo: 8, all_remove:9};
const KeyNum = {enter: 13, end: 35, home: 36, up: 38, down: 40, left: 37, right: 39, backspace: 8};
isFileOpen = false
cursorPos = null
filename = null
memoData = {}

/**
 * データをFlaskに送信する
 * @param {object} data 
 */
function send(data) {
    $.ajax({
        url:addr + "receive",
        type:"POST", 
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'

    }).done(function(res, textStatus, jqXHR ){
        console.log(res.length)
        if (res.length != 0) {
            filename = res[0];
            memoData = res[1];
            isFileOpen = true
        }
        reload(data);

    }).fail(function(jqXHR, textStatus, errorThrown){
        console.log("failed");
        console.log(errorThrown);

    });
}

/**
 * div要素からメモのインデックスを取得する
 * @param {any} element メモの要素
 * @returns number インデックス
 */
function get_memo_idx(element) { return $(element).index(); }

/**
 * データ追加のための情報を整理
 */
function add() { send({type: Type["new"], text: $(':focus').text()}); $("div#last").empty(); }

/**
 * データ編集のための情報を整理
 * @param {bool} down 編集後のカーソル位置が、1つ下か否か
 */
function edit(down=true) { 
    id = get_memo_idx($(':focus').parent().parent().parent());
    if(memoData[get_memo_idx($(':focus').parent().parent().parent())] != $(':focus').text())
        text = $(':focus').text();
        if(down) {
            if(text == "") send({type: Type["edit"], id: id, text: $(':focus').text(), next: id+1});
            else send({type: Type["edit"], id: id, text: $(':focus').text(), next: id+2});
        } else     send({type: Type["edit"], id: id, text: $(':focus').text(), next: id});
}

/**
 * 指定した要素にフォーカスを合わせる
 * @param {any} element フォーカスを合わせる要素
 */
function set_focus(element) {

    // calc cursor position
    pos = cursorPos;
    if(element.text().length < cursorPos) pos = element.text().length;

    // if #last is empty
    if(pos ===0 && element[0].id === "last") {
        setTimeout(() => element.focus(), 0);
        return; 
    }

    // set cursor position
    selection = document.getSelection();
    selection.removeAllRanges(); // remove ranges
    r = document.createRange();
    r.setStart(element[0].firstChild, pos);
    r.setEnd(element[0].firstChild, pos);  
    selection.addRange(r);
}

/**
 * 画面をリロードする
 * @param {object} data Flaskに送信したデータ
 */
function reload(data) {

    if (!isFileOpen) {
        $("#file").text("NO FILE IS OPENED.")
        return
    }


    // update filename
    $('#file').text(filename)

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
            case KeyNum["down"]:
                edit();
                e.preventDefault();
                currentId = get_memo_idx($(':focus').parent().parent().parent());
                if(currentId+1 === memoData.length) set_focus($('div#last'));
                else set_focus($('#container > div.memo:nth-child(' + (currentId+2) + ') > ul > li > div.content'));
                break;

            case KeyNum["up"]:
                edit(false);
                e.preventDefault();
                currentId = get_memo_idx($(':focus').parent().parent().parent());
                if (currentId > 0) set_focus($('#container > div.memo:nth-child(' + (currentId) + ') > ul > li > div.content'));
                break;

            case KeyNum["right"]:
                cursorPos = document.getSelection().focusOffset + 1;
                break;

            case KeyNum["left"]:
                cursorPos = document.getSelection().focusOffset - 1;
                break;

            case KeyNum["home"]:
                cursorPos = 0;
                break;

            case KeyNum["end"]:
                cursorPos = $(':focus').text().length;
                break;

            case KeyNum["backspace"]:
                cursorPos = $(':focus').text().length-1;
                break;

            default:
                cursorPos = document.getSelection().focusOffset + 1;
        }
    })

    $("div.content").click((e) => { cursorPos = document.getSelection().focusOffset; })
    $("button.rm").on("click", (e) => { send({type: Type["remove"], id: get_memo_idx($(e.currentTarget).parent().parent().parent())}) })

    // focus
    switch(data.type){
        case Type["new"]:
            set_focus($('div#last'));
            break;
            
        case Type["edit"]:
            if(memoData.length < data.next) set_focus($('div#last'));
            else set_focus($('#container > div.memo:nth-child(' + (data.next) + ') > ul > li > div.content'));
            break;
    }

}


// element settings
$("div#last").keydown((e) => {
    if(!isFileOpen) return;
    // add
    switch(e.keyCode){
        case KeyNum["enter"]:
            e.preventDefault();
            add();
            break;

        case KeyNum["up"]:
            e.preventDefault();
            if(memoData.length > 0) set_focus($('#container > div.memo:nth-child(' + (memoData.length) + ') > ul > li > div.content'));
            break;
            
        case KeyNum["right"]:
            cursorPos = document.getSelection().focusOffset + 1;
            break;

        case KeyNum["left"]:
            cursorPos = document.getSelection().focusOffset - 1;
            break;
        
        case KeyNum["home"]:
            cursorPos = 0;
            break;

        case KeyNum["end"]:
            cursorPos = $(':focus').text().length;
            break;

        default:
            cursorPos = document.getSelection().focusOffset + 1;
    }
});

$('button#new').click((e) => { send({type: Type["f_new"]}); })
$('button#open').click((e) => { send({type: Type["f_open"]}); })
$('button#undo').click((e) => { send({type: Type["undo"]}); })
$('button#redo').click((e) => { send({type: Type["redo"]}); })
$('button#allRemove').click((e) => { send({type: Type["all_remove"]}); })

// get data from flask and display
send({type: Type["check"]});

//TODO EDITフォーカスが外れたら変更内容をFlaskに送る