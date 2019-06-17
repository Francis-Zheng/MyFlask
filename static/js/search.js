var oUserMes = document.getElementById("answerText");
var oUserResponse_btn = document.getElementById("userResponse_btn");

var oShowDialog = document.getElementById("showDialog");


$("body").keydown(function () {
    if (event.keyCode == "13") {//keyCode=13是回车键
        oUserResponse_btn.onclick();
    }
});

//“发送消息”按钮触发
oUserResponse_btn.onclick = function () {
    var userTextNode = document.createElement("p");
    userTextNode.innerText = "搜索记录：" + oUserMes.value;
    //给div添加文本元素
    oShowDialog.appendChild(userTextNode);
    oShowDialog.scrollTop = oShowDialog.scrollHeight;
    $.ajax({
        type: 'post',
        url: 'query',
        data: {
            queryFromUser: oUserMes.value
        },
        success: function (data) {
            console.log(data);
            var result = JSON.parse(data);
            console.info(result);
            var robotTextNode = document.createElement("p");
            var html = "";
            for (var i = 0; i < result.length; i++){
                console.log(result[i]._id)
                html += "<li><a href="+ result[i].article_url+ " style=\" color:#666; font-size:18px;\">" + result[i].article_url + "<\a>&#160;&#160;" + result[i]._id + "</li>";
            }

            robotTextNode.innerHTML = html;
            oShowDialog.appendChild(robotTextNode);
            oShowDialog.scrollTop = oShowDialog.scrollHeight;
        },
        error: function () {
            var textNode = document.createElement("p");
            textNode.innerHTML = "<li>" + "没有此关键字" + "</li>";
            oShowDialog.appendChild(textNode);
            oShowDialog.scrollTop = oShowDialog.scrollHeight;
            console.log("fail query");
        }
    });
    $("#answerText").val("");
};
