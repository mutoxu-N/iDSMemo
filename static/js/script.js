const addr = "http://127.0.0.1:8080/";
const Type = {new: 1, edit:2, remove:3, check: 4};
const KeyNum = {enter: 13, end: 35, home: 36, up: 38, down: 40, left: 37, right: 39};
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

function get_memo_idx(element) { return $(element).index(); }
function add() { send({type: Type["new"], text: $(':focus').text()}); $("div#last").empty(); }
function edit() { send({type: Type["edit"], id: get_memo_idx($(':focus').parent().parent().parent()), text: $(':focus').text()}); }

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
                cursorPos = document.getSelection().focusOffset;
                e.preventDefault();
                edit();
                break;

            case KeyNum["down"]:
                e.preventDefault();
                currentId = get_memo_idx($(':focus').parent().parent().parent());
                if(currentId+1 === memoData.length) set_focus($('div#last'));
                else set_focus($('#container > div.memo:nth-child(' + (currentId+2) + ') > ul > li > div.content'));
                break;

            case KeyNum["up"]:
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
            set_focus($('#container > div.memo:nth-child(' + (data.id+2) + ') > ul > li > div.content'));
            break;
    }

}


// element settings
$("div#last").keydown((e) => {
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

// get data from flask and display
send({type: Type["check"]});

//TODO EDITフォーカスが外れたら変更内容をFlaskに送る
//TODO div#last から up するとカーソルがうまくいかない