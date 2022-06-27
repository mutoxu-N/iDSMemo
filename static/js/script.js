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
        console.log(data);
        console.log(jqXHR);
        switch(jqXHR.status) {
            case 201:
                setTimeout(() => $('div#last').focus(), 0);
                break;
        }

        memoData = res;
        reload(data);

    }).fail(function(jqXHR, textStatus, errorThrown){
        console.log("failed");

    });
}

function reload(data) {
    console.log($("#container > div.memo "))
    i=0
    switch(data.type){
        case Type["new"]:
            for(i; i<$('#container > div.memo').length; i++){
                e = $("#container > div.memo > ul > li > div.content")[i]
                console.log(e.innerText)
            }
            for(i=$('#container > div.memo').length; i<memoData.length; i++) {
                $('<div class="memo">\
                        <ul style="margin-bottom: 0px;">\
                            <li><div class="content" contenteditable="true">'+ memoData[i] +'</div><button class="rm">削除</button></li>\
                        </ul>\
                    </div>'
                ).insertBefore('div#last')
            }
            break;
        
    }
}


function add() {
    console.log("add")
    send({type: Type["new"], text: currentFocus.text()});        
    $("div#last").empty();
}

function edit() {
    console.log("edit")
    send({type: Type["edit"], id: get_memo_idx(currentFocus.parent().parent().parent()), text: currentFocus.text()});

}

function get_memo_idx(element) {
    return $(element).index();
}


$("div.content").keydown((e) => {
    // edit
    currentFocus = ($(e.currentTarget))
    if (e.keyCode === 13) {
        edit();
        return false;
    }
})


$("div#last").keydown((e) => {
    // add
    currentFocus = ($(e.currentTarget))
    if (e.keyCode === 13) {
        add();
        return false;
    }
});


$("button.rm").on("click", (e) => {
    send({type: Type["remove"], id: get_memo_idx($(e.currentTarget).parent().parent().parent())})
})


//TODO EDITフォーカスが外れたら変更内容をFlaskに送る


// get data from flask and display
send({type: Type["check"]});