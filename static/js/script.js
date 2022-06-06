const addr = "http://127.0.0.1:8080/";
const TYPE = {new: 1, edit:2}

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

$("div#memo").on("click", (e) => {
    var index = $(e.currentTarget).index(); //クリックされた要素のインデックス
    send({type: TYPE["edit"], id: index, text: "b"});
})

$("div.last").on("click", (e) => {
    send({type: TYPE["new"]});
})
