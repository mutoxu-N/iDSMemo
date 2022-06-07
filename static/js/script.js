const addr = "http://127.0.0.1:8080/";
const TYPE = {new: 1, edit:2, remove:3}

function send(data) {

    $.ajax({
        url:addr + "receive",
        type:"POST", 
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'

    }).done(function(data, textStatus, jqXHR ){
        console.log("done");
        console.log(data);

    }).fail(function(jqXHR, textStatus, errorThrown){
        console.log("failed");

    });
    return ""
}

function get_memo_idx(element) {
    return $(element).index();
}


$("div.content").on("click", (e) => {
    send({type: TYPE["edit"], id: get_memo_idx(e.currentTarget), text: "b"});
})

$("div#last").on("click", (e) => {
    send({type: TYPE["new"]});
})

$("button.rm").on("click", (e) => {
    send({type: TYPE["remove"], id: get_memo_idx($(e.currentTarget).parent().parent().parent())})
})


