const addr = "http://127.0.0.1:8080/"

function send() {
    fetch(addr + "add", {methods: "POST"})
        .then((res) => {
            if(!res.ok) throw new Error(`${res.status} ${res.statusText}`)
            return res.blob;
        }).catch((reason) => {
            console.log(reason);
        });
}

$("div#memo").on("click", (e) => {
    var index = $(e.currentTarget).index(); //クリックされた要素のインデックス
    alert(index);
})

// clicked
$("body").on("click", (e) => {
    console.log(e.clickX);
})
