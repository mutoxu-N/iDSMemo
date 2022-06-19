const addr = "http://127.0.0.1:8080/";
const Type = {new: 1, edit:2, remove:3}

currentFocus = null;

function send(data) {
    $.ajax({
        url:addr + "receive",
        type:"POST", 
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'

    }).done(function(data, textStatus, jqXHR ){
        window.location.href = "/";
        console.log("done");
        console.log(data);
        // tmp = $('div#last');
        // setTimeout(() => tmp.focus(), 0);

    }).fail(function(jqXHR, textStatus, errorThrown){
        console.log("failed");

    });
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