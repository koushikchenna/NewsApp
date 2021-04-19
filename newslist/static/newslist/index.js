document.addEventListener('DOMContentLoaded', function(){
});

function reply_click(clicked_id){
    console.log(clicked_id);
    click_id = clicked_id
    uname = document.getElementById(clicked_id).getAttribute("name");
    console.log(uname);
    fetch("allvals/")
        .then(response => response.json())
        .then(resp => {
            console.log(resp);
            for(i = 0; i < Object.keys(resp['resp']).length; i++){
                titlevalue = resp['resp'][clicked_id]
            }
            console.log(titlevalue)
            var str = "bytopicres/" + titlevalue + "/"
            var res = str.split(" ").join("-")
            console.log(res)
            fetch(res)
                .then(response => response.json())
                .then(txt => {
                    //console.log(txt);
                    parseresp(txt)

                })
        });
}
//try .replace() function in js\
function parseresp(txt){
   // event.preventDefault()
    console.log(txt)
    uname = document.getElementById(click_id).getAttribute("name");
    console.log(uname)
    console.log(txt['txt'].length)
    for (x = 0; x < txt['txt'].length; x++){
        //console.log(txt['txt'][x])
        holdval = txt['txt'][x]
        string = "addto/" + holdval + "/" + uname + "/"
        console.log(string)
        fetch(string)
            .then(response => response.json())
            .then(txts => {
                console.log(txts);
            })
    }
}
function down_vote(name){
    console.log(name)
    var val = "remove/" + name + "/"
    var nameedit = val.split(" ").join("-")
    fetch(nameedit)
        .then(response => response.json())
        .then(rmv => {
            console.log(rmv)
        })
}

function info(){
    alert(`Polarity refers to the strength of sentiment inside the text. A polarity score of less than 0.33 would represent a strongly negative article. A polarity score greater than 0.33 usually represents a strongly positive article. Anything in between represents a roughly neutral article. Subjectivity refers to how judgement is shaped in the article by personal opinions and preexisting biases. Values are rated from 0.0 to 1.0 where values closer to 1 are more subjective and 0 are objective.`)
}
function hide(name){
    console.log(name)
    let reveal = document.getElementsByName(name)[0];
    console.log(reveal);
    if (reveal.style.display === "none") {
        reveal.style.display = "block";
    } else {
        reveal.style.display = "none";
    }
}
function spanfunc() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

function hideelem(ident){
    var model = document.getElementById(ident);
    model.style.display = "none";
}

function settingcorona(id){
    //alert(id)
    event.preventDefault()
    fetch("setting/" + id)
    location.reload();
}
function settingsports(id){
    //alert(id)
    event.preventDefault()
    fetch("setting/" + id)
    location.reload();
}
function settingweather(id){
    //alert(id)
    event.preventDefault()
    fetch("setting/" + id)
    location.reload();
}