const addr = "http://127.0.0.1:8080/";
const Type = {new: 1, edit:2, remove:3, check: 4}

currentFocus = null;
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
        currentFocus = ($(e.currentTarget))
        if (e.keyCode === 13) {
            edit();
            return false;
        }
    })
    $("button.rm").on("click", (e) => {
        send({type: Type["remove"], id: get_memo_idx($(e.currentTarget).parent().parent().parent())})
    })
    

    // focus
    switch(data.type){
        case Type["new"]:
            setTimeout(() => $('div#last').focus(), 0);
            console.log($('div#last'));
            break;
        case Type["edit"]:
            setTimeout(() => $('#container > div.memo:nth-child(' + (data.id+2) + ') > ul > li > div.content').focus(), 0);
            console.log($('#container > div.memo:nth-child(' + (data.id+2) + ') > ul > li > div.content'));
            break;
    }

}


function add() {
    send({type: Type["new"], text: currentFocus.text()});        
    $("div#last").empty();
}

function edit() {
    send({type: Type["edit"], id: get_memo_idx(currentFocus.parent().parent().parent()), text: currentFocus.text()});

}

function get_memo_idx(element) {
    return $(element).index();
}




//TODO EDITフォーカスが外れたら変更内容をFlaskに送る
// element settings
$("div#last").keydown((e) => {
    // add
    currentFocus = ($(e.currentTarget))
    if (e.keyCode === 13) {
        add();
        return false;
    }
});

// get data from flask and display
send({type: Type["check"]});